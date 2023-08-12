"""Функции связаные с бд."""

from asgiref.sync import sync_to_async
from aiogram.fsm.context import FSMContext

from culture.models import Exhibit, Route


async def feedback(text: str, state: FSMContext):
    '''Запись отзыва в БД'''


async def get_route_by_name(name: str):
    """Получение маршрута по id."""
    return await Route.objects.aget(name=name)


async def get_exhibit_by_id(route_name: int, exhibit_id: int):
    """Получение экспоната по id. Надо немного изменить модели."""
    route = await get_route_by_name(route_name)
    exhibit = await Exhibit.objects.aget(pk=exhibit_id, route=route,)
    return exhibit


async def get_all_exhibits_by_route(route):
    return await sync_to_async(list)(route.exhibit.all())


async def get_routes() -> list:
    return await sync_to_async(list)(
        Route.objects.values_list('name', flat=True)
    )
