"""Файл с основными функциями, которые нужны для чистоты кода."""

from aiogram.fsm.context import FSMContext


async def get_id_from_state(state: FSMContext) -> tuple[str, int]:
    user_data = await state.get_data()
    route_name = user_data.get('route')
    exhibit_id = int(user_data.get('exhibit'))
    return route_name, exhibit_id


async def speech_to_text_conversion(audiofile) -> str:
    '''
    Конвертация речи в текст.

    Делать буду через speech recognition. Вероятно надо будет аудиофайл
    привести в нужный формат перед конвертацией
    '''
    pass