"""Основные команды бота. Кнопки старт и маршруты"""
from aiogram import F, Router, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    Message,
    ReplyKeyboardRemove,
)
from aiogram.fsm.context import FSMContext

from .config import ADMIN_ID
from .keyboards import (
    make_vertical_keyboard, MAIN_COMMANDS, set_command
)
from .handlers import meetings_router, route_router
from . import message as ms

main_router = Router()
main_router.include_router(meetings_router)
main_router.include_router(route_router)


@main_router.startup()
async def start_bot(bot: Bot):
    await set_command(bot)
    await bot.send_message(ADMIN_ID, 'Бот начал свою работу')


@main_router.shutdown()
async def end_bot(bot: Bot):
    await bot.send_message(ADMIN_ID, 'Бот перестал работать')


@main_router.message(Command("help"))
async def help_info(message: Message) -> None:
    commands = {
        '/start': 'Нажмите для приветсвеного сообщения',
        '/routes': 'Нажмите для выбора маршрута',
        '/cancel': 'Нажмите для отмены команды',
        '/help': 'Нажмите для просмотра доступных команд'
    }
    text = ''
    for command in commands:
        text += f'{command}\n {commands[command]} \n'
    await message.reply(text)


@main_router.message(Command("cancel"))
@main_router.message(F.text.casefold() == "отмена")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=ReplyKeyboardRemove()
    )


@main_router.message(CommandStart())
async def command_main_start(message: Message) -> None:
    """Команда /start. Должна приветствовать пользователя."""
    await message.answer(
        text=ms.GREETING_MESSAGE,
        reply_markup=make_vertical_keyboard(MAIN_COMMANDS)
    )

# Надо исправить
# @meetings_router.message(F.text.in_({'СТАРТ', 'Знакомство', 'Помощь'}))
# async def get_acquainted(message: Message, state: FSMContext) -> None:
#     if message.text == "СТАРТ":
#         await command_start(message, state)
#     elif message.text == "Знакомство":
#         await get_acquainted(message, state)
#     elif message.text == "Помощь":
#         await help_info(message)
