"""Файл с основными функциями, которые нужны для чистоты кода."""
import io
import re

import soundfile as sf
import speech_recognition as speech_r
from aiogram.exceptions import TelegramNetworkError
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile
from aiogram.utils.markdown import hlink
from googlesearch import search

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


async def get_route_from_state(state: FSMContext):
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
        exhibit = await get_exhibit(route_id, exhibit_number)
        await state.update_data(exhibit=exhibit)
        if exhibit.transfer_message != "":
            await message.answer(
                f"{exhibit.transfer_message.replace('<p>', '').replace('</p>', '')}",
                reply_markup=make_row_keyboard(["Отлично идем дальше"]),
            )
        await state.set_state(Route.transition)


async def get_tag_from_description(description: str) -> str:
    """
    Получение хеш-тега из описания и поиск первой ссылки в google по заданному
    тегу.
    Работает через связку Selenium + BeautifulSoup4
    1. Через регулярку ищем в полученном на вход тексте хеш-тег
    2. С помощью Selenium эмулируем закрытое окно браузера для прогрузки
    JS, чтобы получить HTML
    3. С помощью BeautifulSoup4 парсим HTML для поиска первой ссылки в поиске
    гугла по-заданному хеш-тегу
    4. Возвращаем ссылку
    """
    pattern = re.search(r'#\w+', description)
    if pattern is None:
        return description.replace('<p>', '').replace('</p>', '')
    text = pattern.group()
    for i in search(text, lang='ru'):
        url = i
        break
    new_text = hlink(text, url)
    return description.replace(
        text, new_text).replace('<p>', '').replace('</p>', '')


async def send_photo(message: Message, image: FSInputFile) -> None:
    """Проверка при отправки фото."""
    try:
        await message.answer_photo(image)
    except TelegramNetworkError:
        await message.answer('Фото нет в media')
