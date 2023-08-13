"""Функции связаные с бд."""

from aiogram.types import User
import requests

# from core.culture.models import FeedBack


async def feedback(text: str, user: User):
    '''
    Запись отзыва в БД

    Надо сделать апи в джанго
    '''
    username = user.username
    text = text
    try:
        userhobby = user.userhobby
    except Exception:
        userhobby = 'Нет хобби в модели'
    data = dict(
        username=username, text=text, userhobby=userhobby
    )
    requests.post('http://127.0.0.1:8000/api/v1/feedbacks/', data=data)


async def get_exhibit(route_id: int, exhibit_id: int):
    pass
