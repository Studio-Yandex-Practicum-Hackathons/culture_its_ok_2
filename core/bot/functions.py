"""Файл с основными функциями, которые нужны для чистоты кода."""
import io
import re

import bleach
import soundfile as sf
import speech_recognition as speech_r
from aiogram.exceptions import TelegramNetworkError
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message
from aiogram.utils.markdown import hlink
from googlesearch import search

from .crud import get_exhibit, get_route_by_id
from .keyboards import make_row_keyboard
from .utils import Route


def delete_tags(string: str) -> str:
    """Удаляет лишные теги."""
    string = bleach.clean(
            string, tags=['u', 'strong', 'em'], strip=True
        ).replace('\n', '', 1)
    return string


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
    user_data = await state.get_data()
    exhibit = user_data.get("exhibit")
    route_id = user_data.get("route")
    exhibit_number = int(user_data.get("exhibit_number"))
    exhibit_number += 1
    await state.update_data(exhibit_number=exhibit_number)
    route = await get_route_by_id(route_id)
    count_exhibits = user_data.get("count_exhibits")
    if exhibit_number == count_exhibits:
        await message.answer(
            f"На этом медитация по маршруту «{route.name}» окончена.\n"
            "Администрация фестиваля «Ничего страшного» благодарит"
            " вас за использование нашего бота!",
            reply_markup=make_row_keyboard(["Конец"]),
        )
        await state.set_state(Route.quiz)
    else:
        exhibit = await get_exhibit(route_id, exhibit_number)
        await state.update_data(exhibit=exhibit)
        if exhibit.transfer_message != "":
            await message.answer(
                f"{delete_tags(exhibit.transfer_message)}",
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
    description = delete_tags(description)
    pattern = re.search(r'#\w+', description)
    if pattern is None:
        return description
    text = pattern.group()
    for i in search(text, lang='ru'):
        url = i
        break
    new_text = hlink(text, url)
    return description.replace(
        text, new_text)


async def send_photo(message: Message, image: FSInputFile) -> None:
    """Проверка при отправки фото."""
    try:
        await message.answer_photo(image)
    except TelegramNetworkError:
        await message.answer('Фото нет в media')
    except Exception as e:
        await message.answer(e)
