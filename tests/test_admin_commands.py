from unittest.mock import AsyncMock, MagicMock
from aiogram import types
import pytest
from  bot.admin.admin_keyboards import admin_main_kb
from bot.admin.admin_commands import admin_menu


@pytest.mark.asyncio
async def test_admin_menu_success():
    message = AsyncMock(spec=types.Message)
    message.from_user = MagicMock(spec=types.User)
    message.from_user.id = 12345

    message.answer = AsyncMock()

    await admin_menu(message)
    message.answer.assert_called_with('Выбери действие',reply_markup=admin_main_kb)

@pytest.mark.asyncio
async def test_admin_fail():
    message = AsyncMock(spec=types.Message)
    message.from_user = MagicMock(spec=types.User)
    message.from_user.id = 9999

    message.answer = AsyncMock()
    await admin_menu(message)

    message.answer.assert_called_with(
        'Не корректное сообщение.\n\n<b>Нажмите</b> /start для запуска приложения 🐝',
        parse_mode="HTML")

