"""Основные команды бота. Кнопки старт и маршруты"""
from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from bot import message as ms
from bot.config import ADMIN_ID
from bot.handlers import meetings_router, route_router
from bot.keyboards import set_command
from bot.utils import User

main_router = Router()
main_router.include_router(meetings_router)
main_router.include_router(route_router)


@main_router.startup()
async def start_bot(bot: Bot) -> None:
    """
    Срабатывает когда бот начал свою работу
    и оповещает администратора об этом.
    Выводит кнопку меню
    """
    await set_command(bot)
    await bot.send_message(ADMIN_ID, "Бот начал свою работу")


@main_router.shutdown()
async def end_bot(bot: Bot) -> None:
    """
    Срабатывает когда бот закончил свою работу
    и оповещает администратора об этом
    """
    await bot.send_message(ADMIN_ID, "Бот перестал работать")


@main_router.message(Command("help"))
@main_router.message(F.text == "Помощь")
async def help_info(message: Message) -> None:
    """Команда /help выводит все возможные команды."""
    commands = {
        "/start": "Нажмите для приветсвеного сообщения",
        "/routes или Маршруты": "Нажмите для выбора маршрута",
        "/cancel или Помощь": "Нажмите для отмены команды",
        "/help": "Нажмите для просмотра доступных команд"
    }
    text = ''
    for command in commands:
        text += f'{command}\n {commands[command]} \n'
    await message.reply(text)


@main_router.message(Command("cancel"))
@main_router.message(F.text.casefold() == "отмена")
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    """Команда /cancel. Отменяет все действия и возвращает на начало."""
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=ReplyKeyboardRemove()
    )


@main_router.message(CommandStart())
async def command_main_start(message: Message, state: FSMContext) -> None:
    """Команда /start. Должна приветствовать пользователя."""
    await message.answer(
        text=ms.GREETING_MESSAGE,
    )
    await message.answer("Давай познакомимся.\nКак тебя зовут?")
    await state.set_state(User.name)
