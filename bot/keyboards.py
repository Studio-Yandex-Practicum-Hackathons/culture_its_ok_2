"""Файл с основным наборами кнопок у пользователя.
Например набор кнопок yes, no у функции exhibit, должен быть тут."""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

KEYBOARD_YES_NO = [[KeyboardButton(text="Yes"), KeyboardButton(text="No"), ]]
REVIEW_KEYBOARD = [[
    KeyboardButton(text="Отлично! Идем дальше"),
    KeyboardButton(text="No"),
]]


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)
