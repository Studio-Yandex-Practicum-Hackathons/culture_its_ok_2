"""Функции связаные с бд."""

from aiogram.fsm.context import FSMContext

def get_number_routes()-> int:
    '''Получает количество маршрутов'''
    quantity = 3
    return quantity

def get_route_index(index: int) -> dict:
    '''
    возражает путь по индексу
    тут возвращаю словарь для проверки а так вообще объект пути с экспонатами
    '''
    index = 0
    return {'exhibits':[
        ['Экспонат 1', 'Описание 1'],
        ['Экспонат 2', 'Описание 2'],
        ['Экспонат 3', 'Описание 3'],
    ]}

async def feedback(text: str, state: FSMContext):
    '''Запись отзыва в БД'''


async def get_exhibit(route_id: int, exhibit_id: int):
    pass
