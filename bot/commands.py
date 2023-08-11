"""Основные команды бота. Кнопки старт и маршруты"""
import asyncio

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message,  ReplyKeyboardMarkup, KeyboardButton

from functions import get_id_from_state
from crud import get_exhibit
from utils import Route
from keyboards import make_row_keyboard

form_router = Router()

available_routes = ['1', '2', '3']
available_exhibit = ['11', '12', '131']


@form_router.message(Command("start"))
async def command_start(message: Message, state: FSMContext) -> None:
    """Команда /start. Должна приветствовать пользователя."""
    await message.answer(
        text="Hi there! Выбери марштур",
        reply_markup=make_row_keyboard(available_routes),
    )
    await state.set_state(Route.route)


@form_router.message(Route.route)
async def route(message: Message, state: FSMContext) -> None:
    """Отрпавляет сообщение с выбранным маршрутом,
    запускается если есть состояние Route.route.
    Чек лист 4.2.1
    """
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
    """
    Отрпавляет сообщение с экспонатом, запускается если
    есть состояние Route.exhibit и пользователь нажал
    на кнопку да(должно быть 'Отлично! Идем дальше' ??).
    Чек лист 4.7.1-4.7.2.
    """
    user_data = await state.get_data()
    number_exhibit = user_data['exhibit'] + 1
    await state.update_data(exhibit=number_exhibit)
    await message.answer(
        f"QQQQВы на марштруте  {user_data.get('route')}"
        f" и экспонате {number_exhibit}",
    )
    await message.answer('Заполни отзыв на экспонат')
    await state.set_state(Route.review)
    # await review(message, state)


@form_router.message(Route.review)
async def review(message: Message, state: FSMContext) -> None:
    """Отрпавляет сообщение с просьбой написать отзыв, запускается если
    есть состояние Route.review.
    Чек лист 4.5 - 4.7.2.
    В конце должен вызвать функцию, которая выводит следующий экспонат.
    На данный момент это exhibit_yes.
    """
    await message.answer(f'ваш отзыв - {message.text}')
    await message.answer(
        'Cпасибо за отзыв \n Перейти к следующему экспонату?',
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
    # сначала обнуляем состояние отзыва
    await state.set_state(None)
    # потом ставим состояние экспоната
    await state.set_state(Route.exhibit)


@form_router.message(Route.quiz)
async def quiz(message: Message, state: FSMContext) -> None:
    """Отрпавляет сообщение с просьбой пройти опрос, запускается если
    есть состояние Route.quiz.
    Чек лист 7-8.1.1.
    В конце должен вызвать функцию, которая выводит активные марштруты.
    (На данный момент это кнопка start, но кнопка старт
    должна только приветствовать пользователя в начале)
    """
    pass


@form_router.message(Route.exhibit,  F.text.casefold() == "no")
async def exhibit_no(message: Message, state: FSMContext) -> None:
    """
    Отрпавляет сообщение если пользователь
    нажал на кнопку нет, при активном Route.exhibit.
    Должен вывести карту (смотри чек лист 4.3.1 - 4.3.2)
    Так же должен вызывать функцию ( чек лист 4.4)
    """
    user_data = await state.get_data()
    await message.answer(
        f"Выюрано НЕТ .... Вы ушли с марштура {user_data['route']} ",
        reply_markup=make_row_keyboard(available_routes)
    )
    await state.clear()


@form_router.message(Route.exhibit)
async def exhibit(message: Message, state: FSMContext) -> None:
    """
    Отрпавляет сообщение с первым экспонатом, запускается если
    есть состояние Route.exhibit.
    В чек листе нет.
    (Надо подумать нужна ли она.)
    """
    await state.update_data(exhibit=1)
    route_id, exhibit_id = await get_id_from_state(state)
    await get_exhibit(route_id, exhibit_id)
    await message.answer(
        f"Вы на марштруте  {route_id}"
        f" и экспонате {exhibit_id} \n"
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
    """Ловит все сообщения от пользователя,
    если они не попадают под условиях функций выше.
    Она нам не нужна.
    """
    await message.answer(message.text)
