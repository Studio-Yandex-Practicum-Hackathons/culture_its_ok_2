"""Файл с основными функциями, которые нужны для чистоты кода."""
import io

import soundfile as sf
import speech_recognition as speech_r
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from ..culture.models import Route as Route_object
from .crud import get_all_exhibits_by_route, get_exhibit, get_route_by_id
from .keyboards import make_row_keyboard
from .utils import Route


async def get_id_from_state(state: FSMContext) -> tuple[str, int]:
    """Полученние имени маршрута и номера экспоната из state."""
    user_data = await state.get_data()
    route_name = user_data.get("route")
    exhibit_number = int(user_data.get("exhibit_number"))
    return route_name, exhibit_number


async def get_exhibit_from_state(state: FSMContext):
    """Полученние экспоната из state."""
    user_data = await state.get_data()
    return user_data.get("exhibit")


async def get_route_from_state(state: FSMContext) -> Route_object:
    """Полученние маршрута из state."""
    user_data = await state.get_data()
    return user_data.get("route_obj")


async def speech_to_text_conversion(filename) -> str:
    """
    Конвертация речи в текст.

    Делать буду через speech recognition. Вероятно надо будет аудиофайл
    привести в нужный формат перед конвертацией
    1. Привести файл в нужный формат.
    2. Конвертация в текст
    """
    recogniser = speech_r.Recognizer()
    data, samplerate = sf.read(filename)
    voice_file = io.BytesIO()
    sf.write(voice_file, data, samplerate, format="WAV", subtype="PCM_16")
    voice_file.seek(0)
    audio_file = speech_r.AudioFile(voice_file)
    with audio_file as source:
        audio = recogniser.record(source)
    return recogniser.recognize_google(audio, language="ru-RU")


async def set_route(state: FSMContext, message: Message) -> None:
    """
    Устанавливает состояние Route в зависимости кончился маршрут или нет.
    """
    exhibit = await get_exhibit_from_state(state)
    route_id, exhibit_number = await get_id_from_state(state)
    exhibit_number += 1
    await state.update_data(exhibit_number=exhibit_number)
    route = await get_route_by_id(route_id)
    if exhibit_number == len(await get_all_exhibits_by_route(route)):
        await message.answer(
            "Конец маршрута",
            reply_markup=make_row_keyboard(["Конец"]),
        )
        await state.set_state(Route.quiz)
    else:
        if exhibit.transfer_message != "":
            await message.answer(
                f"{exhibit.transfer_message}",
            )
        await message.answer(
            "Нас ждут длительные переходы",
            reply_markup=make_row_keyboard(["Отлично идем дальше"]),
        )
        exhibit = await get_exhibit(route_id, exhibit_number)
        await state.update_data(exhibit=exhibit)
        await state.set_state(Route.transition)
