from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from .. import message as ms
from ..keyboards import MAIN_COMMANDS, make_vertical_keyboard, HOBBY
from ..utils import User
from ..validators import check_age, check_name

meetings_router = Router()


@meetings_router.message(User.name)
async def get_name(message: Message, state: FSMContext) -> None:
    """Получает имя пользователя"""
    if await check_name(message.text):
        await state.update_data(username=message.text)
        await message.answer(ms.AGE_MESSAGE)
        await state.set_state(User.age)
    else:
        await message.answer(ms.NAME_ERROR)
        await state.set_state(User.name)


@meetings_router.message(User.age)
async def get_age(message: Message, state: FSMContext) -> None:
    """Получает возраст пользователя"""
    if await check_age(message.text):
        await state.update_data(userage=int(message.text))
        await message.answer(
            ms.HOBBY_MESSAGE,
            reply_markup=make_vertical_keyboard(HOBBY)
        )
        await state.set_state(User.hobby)
    else:
        await message.answer(ms.AGE_ERROR)
        await message.answer(ms.AGE_MESSAGE)


@meetings_router.message(User.hobby, F.text == 'другое')
async def get_hobby_another(message: Message, state: FSMContext) -> None:
    """Получает хобби пользователя"""
    await state.update_data(userhobby=message.text)
    data = await state.get_data()
    name = data.get('username')
    await message.answer(
        ms.END_ACQUAINTANCE.format(name),
        reply_markup=make_vertical_keyboard(MAIN_COMMANDS)
    )
    await state.set_state(None)


@meetings_router.message(User.hobby, F.text.in_(HOBBY))
async def get_hobby(message: Message, state: FSMContext) -> None:
    """Получает хобби пользователя"""
    await state.update_data(userhobby=message.text)
    data = await state.get_data()
    name = data.get('username')
    await message.answer(
        ms.END_ACQUAINTANCE.format(name),
        reply_markup=make_vertical_keyboard(MAIN_COMMANDS)
    )
    await state.set_state(None)
