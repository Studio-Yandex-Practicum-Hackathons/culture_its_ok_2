"""Основные команды бота. Кнопки старт и маршруты"""
import asyncio

from aiogram.filters import CommandStart
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
)
import message as mes
from functions import get_id_from_state, add_user_information,speech_to_text_conversion
from crud import feedback, get_number_routes, get_route_index
from validators import check_name, check_age, feedback_validator
from utils import Route, User
from keyboards import make_row_keyboard, KEYBOARD_YES_NO, REVIEW_KEYBOARD, KEYBOARD_START, make_vertical_keyboard

form_router = Router()

available_routes = [f'Маршрут {i+1}'for i in range(get_number_routes())]
main_batten = ["СТАРТ", 'Знакомство', 'help']


@form_router.message(CommandStart())
async def command_start(message: Message) -> None:
    """Команда /start. Должна приветствовать пользователя."""
    await message.answer(
        mes.hello,
        reply_markup=make_vertical_keyboard(main_batten)
    )


@form_router.message(Command(commands=["cancel"]))
@form_router.message(F.text.casefold() == "отмена")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=ReplyKeyboardRemove()
    )

@form_router.message(F.text == "Знакомство")
async def get_acquainted(message: Message, state: FSMContext) -> None:
    '''Знакомство'''
    await message.answer("Давай познакомимся.\nКак тебя зовут?")
    await state.set_state(User.name)


@form_router.message(User.name)
async def get_name(message: Message, state: FSMContext) -> None:
    """Получает имя пользователя"""
    if await check_name(message.text):
        await state.update_data(name=message.text)
        await message.answer(mes.age)
        await state.set_state(User.age)
    else:
        await message.answer('Некорректное имя. Еше раз')
        await state.set_state(User.name)


@form_router.message(User.age)
async def get_age(message: Message, state: FSMContext) -> None:
    """Получает возраст пользователя"""
    if await check_age(message.text):
        await state.update_data(age=message.text)
        await message.answer(mes.hobby)
        await state.set_state(User.hobby)
    else:
        await message.answer('Некорректный возраст')
        await message.answer(mes.age)


@form_router.message(User.hobby)
async def get_hobby(message: Message, state: FSMContext) -> None:
    """Получает хобби пользователя"""
    await state.update_data(hobby=message.text)
    await add_user_information(state)
    await message.answer(
        'Приятно познакомится',
        reply_markup=make_vertical_keyboard(main_batten)
    )
    await state.clear()


@form_router.message(F.text == "СТАРТ")
async def choice_route(message: Message, state: FSMContext) -> None:
    '''Выбор маршрута'''
    await message.answer(
        mes.map_information,
        reply_markup=make_vertical_keyboard(available_routes)
    )
    # тут должна быть карта фестиваля
    await state.set_state(Route.route)


@form_router.message(Route.route,  F.text.casefold() == "нет")
async def start_proute(message: Message, state: FSMContext) -> None:
    '''Поиск маршрута'''
    await message.answer('Медитация по адресу')
    await message.answer('вы стоите в начале',
            reply_markup=make_row_keyboard(['да']),
            )


@form_router.message(Route.route,  F.text.casefold() == 'да')
async def start_path(message: Message, state: FSMContext) -> None:
    '''Старт медитации'''
    await state.update_data(exhibit_number=1)
    await message.answer(
        'Отлично начнем нашу медитацию',
        reply_markup=make_row_keyboard(['Отлично начинаем'])
    )
    await state.set_state(Route.exhibit)


@form_router.message(Route.route)
async def route_info(message: Message, state: FSMContext) -> None:
    """Начало пути """
    await message.answer('Описания маршрута')
    await state.update_data(route=get_route_index(message.text))
    await message.answer(mes.start_route,
            reply_markup=ReplyKeyboardMarkup(
            keyboard=KEYBOARD_YES_NO,
            resize_keyboard=True,)
            )

@form_router.message(Route.exhibit)
async def exhibit_information(message: Message, state: FSMContext) -> None:
    '''Обзор экспонат'''
    data = await state.get_data() 
    await message.answer(
        f'Про экспонат {data["route"]["exhibits"][data["exhibit_number"]-1][1]}'
    )
    await message.answer(
        'о чем думаете Опишите',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Route.review)


@form_router.message(Route.review, F.voice | F.text)
async def review(message: Message, state: FSMContext) -> None:
    '''Получения отзыва'''
    if message.voice:
        text = await feedback_validator(speech_to_text_conversion(message.voice))
    elif message.text:
        text = await feedback_validator(message.text)
    await feedback(text, state)
    await message.answer('Спасибо за ваше наюддение')
    data = await state.get_data()
    number_exhibit = data['exhibit_number'] + 1
    await state.update_data(exhibit_number=number_exhibit)
    if data['exhibit_number'] >= len(data['route']["exhibits"]):
        await message.answer(
            'Конец маршрута',
            reply_markup=make_row_keyboard(['Конец']),
        )
        await state.set_state(Route.quiz)
    else:
        await message.answer(
            'Нас ждут длительные переходы',
            reply_markup=make_row_keyboard(['Отлично идем дальше']),
        )
        await state.set_state(Route.transition)


@form_router.message(Route.transition)
async def transition(message: Message, state: FSMContext) -> None:
    '''Переход'''
    await message.answer(
        'Следующий объект по адресу. Получилось найти',
        reply_markup=make_row_keyboard(['Да'])
    )
    # Картинка экспоната
    await state.set_state(Route.exhibit)


@form_router.message(Route.quiz)
async def end_route(message: Message, state: FSMContext) -> None:
    '''Конец маршрута'''
    await message.answer('Клманда будет рада отклику\nСсылка на форму')
    await state.clear()
    await message.answer(
        'Вернутся на выбор маршрута',
        reply_markup=make_row_keyboard(['СТАРТ'])
    )


@form_router.message(F.text =="help")
async def help_info(message: Message) -> None:
    await message.answer('Тут описаны подсказки')

@form_router.message()
async def bot_echo(message: Message):
    """Ловит все сообщения от пользователя,
    если они не попадают под условиях функций выше.
    Она нам не нужна.
    """
    await message.answer(message.text)
