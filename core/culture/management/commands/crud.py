"""Функции связаные с бд."""

from aiogram.fsm.context import FSMContext

from culture.models import Exhibit


async def feedback(text: str, state: FSMContext):
    '''Запись отзыва в БД'''


async def get_exhibit(route_id: int, exhibit_id: int):
    exhibit = await Exhibit.objects.aget(pk=exhibit_id, route=route_id,)
    return exhibit
