"""Функции связаные с бд."""

from asgiref.sync import sync_to_async
from aiogram.fsm.context import FSMContext

from culture.models import Route, Review


async def get_route_by_name(name: str):
    """Получение маршрута по id."""
    return await Route.objects.aget(name=name)


async def get_exhibit_by_id(route_name: str, exhibit_number: int):
    """Получение экспоната по id. Надо немного изменить модели.
    Надо исправить"""
    route = await get_route_by_name(route_name)
    exhibit = (await get_all_exhibits_by_route(route))[exhibit_number]
    print(exhibit)
    return exhibit


async def feedback(text: str, state: FSMContext):
    '''Запись отзыва в БД'''
    data = await state.get_data()
    exhibit = await get_exhibit_by_id(
        data.get('route'),
        data.get('exhibit_number')
    )
    await Review.objects.acreate(text=text, exhibit=exhibit)


async def get_all_exhibits_by_route(route):
    """Получение всех экспонатов у данного маршрута."""
    return await sync_to_async(list)(route.exhibite.all())


async def get_routes() -> list:
    """Получение списка имен марштуров"""
    return await sync_to_async(list)(
        Route.objects.values_list('name', flat=True)
    )
