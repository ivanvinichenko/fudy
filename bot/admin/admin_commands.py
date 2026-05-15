from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


from bot.admin.admin_handlers import broadcast_message_celery
from bot.admin.admin_keyboards import admin_main_kb
from bot.admin.admin_states import MailingStates
from core.setup import router

admin_ids = [7712168206,8165802627,12345]
@router.message(F.text == 'admin')
async def admin_menu(message: types.Message):
    tg_id = message.from_user.id
    if tg_id in admin_ids:
        await message.answer('Выбери действие',reply_markup=admin_main_kb)
    else:
        await message.answer("Не корректное сообщение."
                             "\n\n<b>Нажмите</b> /start для запуска приложения 🐝",
                             parse_mode="HTML")

@router.callback_query(F.data == 'admin:create_mailing')
async def handle_create_mailing(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    await callback.message.answer(
        "Пришли полное сообщение рассылки.\n"
        "Можно текст, фото+текст и т.п. — начнём с текста."
    )
    await state.set_state(MailingStates.waiting_text)


@router.message(MailingStates.waiting_text)
async def mailing_get_text(message: Message, state: FSMContext):
    mailing_text = message.text
    admin_id = message.from_user.id

    await state.update_data(mailing_text=mailing_text)

    await message.answer("Принял текст рассылки. Начинаю рассылку...")

    broadcast_message_celery.delay(
        text=mailing_text,
        disable_notification=False,
        chunk_size=30,
        delay_between_chunks=1.0,
        admin_id=admin_id,
    )

    await state.clear()


