"""Файл с основными функциями, которые нужны для чистоты кода."""

from aiogram.fsm.context import FSMContext


async def get_id_from_state(state: FSMContext) -> tuple(int, int):
    user_data = await state.get_data()
    route_id = user_data.get('route')
    exhibit_id = user_data.get('exhibit')
    return route_id, exhibit_id
