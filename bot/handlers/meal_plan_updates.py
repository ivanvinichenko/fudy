from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
import logging

from bot.Gemini.requests import generate_meal_plan, parse_meal_plan
from database.models import User, async_session, MealUserInfo, MealUserPlan


async def update_meal_plan(user: User):
    try:
        async with async_session() as session:
            result = await session.execute(
                select(MealUserInfo).where(MealUserInfo.user_id == user.tg_id)
            )
            meal_info = result.scalar_one_or_none()
            last_day_result = await session.execute(
                select(func.max(MealUserPlan.day_number)).where(MealUserPlan.user_id == user.tg_id)
            )
            last_day_number = last_day_result.scalar() or 0
            full_plan = await generate_meal_plan(user, None, 7)
            plan_data = parse_meal_plan(full_plan)

            if not meal_info:
                meal_info = MealUserInfo(user_id=user.tg_id)
                session.add(meal_info)

            for offset, (day_number, day_info) in enumerate(plan_data["days"].items(), start=1):
                new_day_number = last_day_number + offset
                day_plan = MealUserPlan(
                    user_id=user.tg_id,
                    day_number=new_day_number,
                    meal_text=day_info["raw_text"]
                )
                session.add(day_plan)

            meal_info.updated_at = datetime.now()
            await session.commit()

            return full_plan
    except Exception as e:
        print(e)
        return None



async def nightly_plan_update():
    async with async_session() as session:
        try:
            result = await session.execute(
                select(User).options(selectinload(User.meal_plan))
                .where(User.meal_plan.any())
            )
            users = result.scalars().all()
            print(f"Найдено пользователей: {len(users)}")

            for user in users:
                try:
                    await update_meal_plan(user)
                    print("Обновлен план для пользователя: ", user.last_name)
                except Exception as e:
                    logging.error(f"Ошибка обновления плана для {user.tg_id}: {e}")
        except Exception as e:
            logging.error(f"Общая ошибка в nightly_plan_update: {e}")
