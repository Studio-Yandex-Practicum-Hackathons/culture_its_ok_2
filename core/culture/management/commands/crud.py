"""Функции связаные с бд."""

from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async
from culture.models import Review, Route


async def get_routes_name() -> list:
    """Получение списка имен марштуров"""
    return await sync_to_async(list)(
        Route.objects.values_list('name', flat=True)
    )


async def get_routes_id() -> list:
    """Получение списка имен марштуров"""
    return await sync_to_async(list)(
        Route.objects.values_list('id', flat=True)
    )


async def get_route_by_id(id: str):
    """Получение маршрута по id."""
    return await Route.objects.aget(id=id)


async def get_route_by_name(name: str):
    """Получение маршрута по name."""
    return await Route.objects.aget(name=name)


async def get_exhibit(route_id: str, exhibit_number: int):
    """Получение экспоната по id. Надо немного изменить модели.
    Надо исправить"""
    route = await get_route_by_id(route_id)
    exhibit = (await get_all_exhibits_by_route(route))[exhibit_number]
    print(exhibit)
    return exhibit


async def save_review(text: str, state: FSMContext):
    '''Запись отзыва в БД'''
    data = await state.get_data()
    exhibit = await get_exhibit(
        data.get('route'),
        data.get('exhibit_number')
    )
    await Review.objects.acreate(text=text, exhibit=exhibit)


async def get_all_exhibits_by_route(route):
    """Получение всех экспонатов у данного маршрута."""
    return await sync_to_async(list)(route.exhibite.all())
