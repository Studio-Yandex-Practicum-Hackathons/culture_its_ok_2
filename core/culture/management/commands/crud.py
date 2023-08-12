"""Функции связаные с бд."""

from asgiref.sync import sync_to_async
from aiogram.fsm.context import FSMContext

from culture.models import Exhibit, Route


async def feedback(text: str, state: FSMContext):
    '''Запись отзыва в БД'''


async def get_route_by_id(route_id: int):
    """Получение маршрута по id."""
    return await Route.objects.aget(pk=route_id)


async def get_exhibit_by_id(route_id: int, exhibit_id: int):
    """Получение экспоната по id. Надо немного изменить модели."""
    exhibit = await Exhibit.objects.aget(pk=exhibit_id, route=route_id,)
    return exhibit


async def get_all_exhibits_by_route(route):
    return await sync_to_async(list)(route.route.all())
