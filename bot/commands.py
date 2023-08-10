"""Основные команды бота. Кнопки старт и маршруты"""
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message,  ReplyKeyboardMarkup, KeyboardButton

from utils import Route

form_router = Router()


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


available_routes = ['1', '2', '3']
available_exhibit = ['11', '12', '131']


@form_router.message(Command("start"))
async def command_start(message: Message, state: FSMContext) -> None:
    await message.answer(
        text="Hi there! Выбери марштур",
        reply_markup=make_row_keyboard(available_routes),
    )
    await state.set_state(Route.route)


@form_router.message(Route.route)
async def route(message: Message, state: FSMContext) -> None:
    await state.update_data(route=message.text.lower())
    user_data = await state.get_data()
    await state.set_state(Route.exhibit)
    await message.answer(
        f"Вы выбрали марщтур  {user_data['route']}",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Yes"),
                    KeyboardButton(text="No"),
                ]
            ],
            resize_keyboard=True,
        ),
    )


@form_router.message(Route.exhibit,  F.text.casefold() == "yes")
async def exhibit_yes(message: Message, state: FSMContext) -> None:
    user_data = await state.get_data()
    await message.answer(
        f"Вы на марштруте  {user_data['route']} и экспонате ...",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Yes"),
                    KeyboardButton(text="No"),
                ]
            ],
            resize_keyboard=True,
        ),
    )
    await state.clear()


@form_router.message(Route.exhibit,  F.text.casefold() == "no")
async def exhibit_no(message: Message, state: FSMContext) -> None:
    user_data = await state.get_data()
    await message.answer(
        f"Выюрано НЕТ .... Вы на марштруте  {user_data['route']} "
    )
    await state.clear()


@form_router.message()
async def bot_echo(message: Message):
    await message.answer(message.text)
