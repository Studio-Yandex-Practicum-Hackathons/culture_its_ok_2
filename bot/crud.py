"""Функции связаные с бд."""

from aiogram.fsm.context import FSMContext


async def feedback(text: str, state: FSMContext):
    '''Запись отзыва в БД'''


async def get_exhibit(route_id: int, exhibit_id: int):
    pass
