"""Функции связаные с бд."""

from aiogram.types import User

# from core.culture.models import FeedBack


async def feedback(text: str, user: User):
    '''
    Запись отзыва в БД

    Надо сделать апи в джанго
    '''
    username = user.username
    text = text


async def get_exhibit(route_id: int, exhibit_id: int):
    pass
