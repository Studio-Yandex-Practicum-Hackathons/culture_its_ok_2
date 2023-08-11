"""Функции связаные с бд."""
from ..core.culture.models import Exhibit


async def get_exhibit(route_id: int, exhibit_id: int):
    exhibit = await Exhibit.objects.aget(route=route_id, pk=exhibit_id)
    print(exhibit)
    return exhibit
