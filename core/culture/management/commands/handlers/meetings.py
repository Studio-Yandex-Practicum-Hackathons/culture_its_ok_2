from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message
)

from ..functions import (
    add_user_information
)

from ..utils import User
from ..keyboards import (
    make_vertical_keyboard, MAIN_COMMANDS
)
from .. import message as ms
from ..validators import (check_name, check_age)

meetings_router = Router()


@meetings_router.message(Command('acquaintance'))
async def get_acquainted(message: Message, state: FSMContext) -> None:
    '''Знакомство'''
    await message.answer("Давай познакомимся.\nКак тебя зовут?")
    await state.set_state(User.name)


@meetings_router.message(User.name)
async def get_name(message: Message, state: FSMContext) -> None:
    """Получает имя пользователя"""
    if await check_name(message.text):
        await state.update_data(name=message.text)
        await message.answer(ms.AGE_MESSAGE)
        await state.set_state(User.age)
    else:
        await message.answer('Некорректное имя. Еше раз')
        await state.set_state(User.name)


@meetings_router.message(User.age)
async def get_age(message: Message, state: FSMContext) -> None:
    """Получает возраст пользователя"""
    if await check_age(message.text):
        await state.update_data(age=message.text)
        await message.answer(ms.HOBBY_MESSAGE)
        await state.set_state(User.hobby)
    else:
        await message.answer('Некорректный возраст')
        await message.answer(ms.AGE_MESSAGE)


@meetings_router.message(User.hobby)
async def get_hobby(message: Message, state: FSMContext) -> None:
    """Получает хобби пользователя"""
    await state.update_data(hobby=message.text)
    await add_user_information(state)
    await message.answer(
        'Приятно познакомится',
        reply_markup=make_vertical_keyboard(MAIN_COMMANDS)
    )
    await state.set_state(None)


# Надо исправить
# @meetings_router.message(F.text.in_({'СТАРТ', 'Знакомство', 'Помощь'}))
# async def get_acquainted(message: Message, state: FSMContext) -> None:
#     if message.text == "СТАРТ":
#         await command_start(message, state)
#     elif message.text == "Знакомство":
#         await get_acquainted(message, state)
#     elif message.text == "Помощь":
#         await help_info(message)
