"""Файл с основными функциями, которые нужны для чистоты кода."""

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import speech_recognition as speech_r
import soundfile as sf

from .config import BASE_DIR


async def add_user_information(state: FSMContext) -> None:
    '''
    Добавляет информацию о пользователе в пдф файл
    '''
    return None


async def get_id_from_state(state: FSMContext) -> tuple[str, int]:
    """Полученние имени маршрута и номера экспоната из state."""
    user_data = await state.get_data()
    route_name = user_data.get('route')
    exhibit_number = int(user_data.get('exhibit_number'))
    return route_name, exhibit_number


# как я понял тут пока что старая версия функции
# после созвона исправим версию
async def speech_to_text_conversion(filename: str, message: Message) -> str:
    '''
    Конвертация речи в текст.

    Делать буду через speech recognition. Вероятно надо будет аудиофайл
    привести в нужный формат перед конвертацией
    1. Привести файл в нужный формат.
    2. Конвертация в текст
    '''
    recogniser = speech_r.Recognizer()
    data, samplerate = sf.read(f'{BASE_DIR}/tmp/voices/{filename}.ogg')
    sf.write(f'{BASE_DIR}/tmp/voices/{filename}.wav', data, samplerate)
    audio_file = speech_r.AudioFile(f'{BASE_DIR}/tmp/voices/{filename}.wav')
    with audio_file as source:
        audio = recogniser.record(source)
    return recogniser.recognize_google(audio, language='ru-RU')
