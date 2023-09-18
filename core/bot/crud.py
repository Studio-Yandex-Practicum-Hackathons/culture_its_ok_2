"""Функции связаные с бд."""

from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async

from culture.models import Exhibit, Photo, Review, Route


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


async def get_route_by_id(id: str) -> Route:
    """Получение маршрута по id."""
    return await Route.objects.aget(id=id)


async def get_route_by_name(name: str) -> Route:
    """Получение маршрута по name."""
    return await Route.objects.aget(name=name)


async def get_exhibit(route_id: str, exhibit_number: int) -> Exhibit:
    """Получение экспоната по id. Надо немного изменить модели."""
    route = await get_route_by_id(route_id)
    exhibit = (await get_all_exhibits_by_route(route))[exhibit_number]
    return exhibit


async def save_review(text: str, state: FSMContext) -> None:
    """Запись отзыва в БД"""
    data = await state.get_data()
    data["text"] = text
    data.pop("route")
    data.pop("exhibit_number")
    data.pop("count_exhibits")
    data.pop("route_obj")
    await Review.objects.acreate(
        **data
    )


async def get_all_exhibits_by_route(route) -> list[Exhibit]:
    """Получение всех экспонатов у данного маршрута."""
    return await sync_to_async(list)(route.exhibite.all())


async def get_all_photos_by_exhibit(exhibit) -> list[Photo]:
    """Получение всех фото у данного эксплгата."""
    return await sync_to_async(list)(exhibit.image.all())
