import asyncio
import logging

from apscheduler.triggers.cron import CronTrigger
from sqlalchemy import select

from bot.Gemini.requests import get_entry_review
from database.models import User, async_session
from core.setup import scheduler

async def send_notifications_22():
    async with async_session() as session:
        result = await session.execute(
            select(User.tg_id))
        tg_ids = list(result.scalars())

    if not tg_ids:
        logging.info("send_notifications_22: нет получателей на сейчас")
        return
    sem = asyncio.Semaphore(20)

    async def _safe_send(uid: int):
        async with sem:
            try:
                await get_entry_review(uid)
            except Exception:
                logging.exception(f"Ошибка при get_entry_review для {uid}")

    await asyncio.gather(*(_safe_send(uid) for uid in tg_ids))


def register_fixed_22_job():
    scheduler.add_job(
        send_notifications_22,
        trigger=CronTrigger(hour=13, minute=20, timezone="Europe/Warsaw"),
        id="fixed_22_notifications",
        replace_existing=True,
    )
