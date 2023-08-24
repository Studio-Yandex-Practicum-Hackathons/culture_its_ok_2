"""Файл с основным наборами кнопок у пользователя."""
from aiogram import Bot
from aiogram.types import (BotCommand, BotCommandScopeDefault,
                           InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

MAIN_COMMANDS = ["/routes", '/help']

HOBBY = ["искусство", "стрит-арт", "фотография", "прогулка", "спорт", "другое"]

KEYBOARD_START = [[KeyboardButton(text="routes"), ]]
KEYBOARD_YES_NO = [[KeyboardButton(text="Да"), KeyboardButton(text="Нет"), ]]
REVIEW_KEYBOARD = [[
    KeyboardButton(text="Отлично! Идем дальше"),
    KeyboardButton(text="Нет"),
]]


async def set_command(bot: Bot):
    commands = [
        BotCommand(
            command="start",
            description="Начало работы бота"
        ),
        BotCommand(
            command="routes",
            description="Выбор маршрута"
        ),
        BotCommand(
            command="help",
            description="справка о командах"
        ),
        BotCommand(
            command="cancel",
            description="Сбросить"
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


def keyboard_yes() -> ReplyKeyboardMarkup:
    """Создаёт реплай-клавиатуру с кнопкой Да"""
    yes = KeyboardButton(text="Да")
    return ReplyKeyboardMarkup(keyboard=[[yes]], resize_keyboard=True)


def keyboard_routes() -> ReplyKeyboardMarkup:
    """Создаёт реплай-клавиатуру с кнопкой /routes"""
    button = KeyboardButton(text='/routes')
    return ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True)


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


def keyboard_for_send_review():
    """
    Создаёт инлайн клавиатуру из двух кнопок.
    """
    buttons = [
        [
            InlineKeyboardButton(
                text="Оставить отзыв", callback_data="send_review"
            ),
            InlineKeyboardButton(
                text="Без отзыва", callback_data="dont_send_review"
            )
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def keyboard_for_transition():
    '''
    Создаёт инлайн клавиатуру из двух кнопок для transition.
    '''
    buttons = [
        [
            InlineKeyboardButton(
                text='На месте', callback_data='in_place'
            ),
            InlineKeyboardButton(
                text='Маршрут', callback_data='route'
            )
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
