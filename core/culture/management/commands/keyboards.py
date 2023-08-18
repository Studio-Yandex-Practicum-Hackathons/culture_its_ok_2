"""Файл с основным наборами кнопок у пользователя.
Например набор кнопок yes, no у функции exhibit, должен быть тут."""
from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

MAIN_COMMANDS = ["/routes", '/Знакомство', '/help']

KEYBOARD_START = [[KeyboardButton(text="routes"), ]]
KEYBOARD_YES_NO = [[KeyboardButton(text="Да"), KeyboardButton(text="Нет"), ]]
REVIEW_KEYBOARD = [[
    KeyboardButton(text="Отлично! Идем дальше"),
    KeyboardButton(text="Нет"),
]]


async def set_command(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Начало работы бота'
        ),
        BotCommand(
            command='routes',
            description='Выбор маршрута'
        ),
        BotCommand(
            command='acquaintance',
            description='Сбор информации о пользователе'
        ),
        BotCommand(
            command='help',
            description='справка о командах'
        ),
        BotCommand(
            command='cancel',
            description='Сбросить'
        ),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault(), 'ru')


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


def make_vertical_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с горизонтальными кнопками
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    vertical_keyboard = []
    for text in items:
        vertical_keyboard.append([KeyboardButton(text=text)])
    return ReplyKeyboardMarkup(
        keyboard=vertical_keyboard, resize_keyboard=True
    )
