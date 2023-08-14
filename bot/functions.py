"""Файл с основными функциями, которые нужны для чистоты кода."""

from aiogram.fsm.context import FSMContext

async def add_user_information(state: FSMContext)-> None:
    '''
    Добавляет информацию о пользователе в пдф файл
    '''
    return None

async def get_id_from_state(state: FSMContext) -> tuple[int, int]:
    user_data = await state.get_data()
    route_id = user_data.get('route')
    exhibit_id = user_data.get('exhibit')
    return route_id, exhibit_id


async def speech_to_text_conversion(audiofile) -> str:
    '''
    Конвертация речи в текст.

    Делать буду через speech recognition. Вероятно надо будет аудиофайл
    привести в нужный формат перед конвертацией
    '''
    pass
