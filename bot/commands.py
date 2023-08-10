"""Основные команды бота. Кнопки старт и маршруты"""
import asyncio

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message,  ReplyKeyboardMarkup, KeyboardButton

from utils import Route
from keyboards import make_row_keyboard

form_router = Router()

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
    )
    await asyncio.sleep(1)
    await exhibit(message, state)


@form_router.message(Route.exhibit,  F.text.casefold() == "yes")
async def exhibit_yes(message: Message, state: FSMContext) -> None:
    user_data = await state.get_data()
    number_exhibit = user_data['exhibit'] + 1
    await state.update_data(exhibit=number_exhibit)
    await message.answer(
        f"QQQQВы на марштруте  {user_data.get('route')}"
        f" и экспонате {number_exhibit}",
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


@form_router.message(Route.exhibit,  F.text.casefold() == "no")
async def exhibit_no(message: Message, state: FSMContext) -> None:
    user_data = await state.get_data()
    await message.answer(
        f"Выюрано НЕТ .... Вы ушли с марштура {user_data['route']} ",
        reply_markup=make_row_keyboard(available_routes)
    )
    await state.clear()


@form_router.message(Route.exhibit)
async def exhibit(message: Message, state: FSMContext) -> None:
    await state.update_data(exhibit=1)
    user_data = await state.get_data()
    await message.answer(
        f"Вы на марштруте  {user_data.get('route')}"
        f" и экспонате {user_data.get('exhibit')} \n"
        f"Нажмите да если хотите перейти к следующему экспонату",
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





@form_router.message()
async def bot_echo(message: Message):
    await message.answer(message.text)
