"""Файл с основными функциями, которые нужны для чистоты кода."""

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import speech_recognition as speech_r
import soundfile as sf


async def get_id_from_state(state: FSMContext) -> tuple[str, int]:
    user_data = await state.get_data()
    route_name = user_data.get('route')
    exhibit_id = int(user_data.get('exhibit'))
    return route_name, exhibit_id


async def speech_to_text_conversion(filename: str, message: Message) -> str:
    '''
    Конвертация речи в текст.

    Делать буду через speech recognition. Вероятно надо будет аудиофайл
    привести в нужный формат перед конвертацией
    1. Привести файл в нужный формат.
    2. Конвертация в текст
    '''
    recogniser = speech_r.Recognizer()
    data, samplerate = sf.read(f'/tmp/{filename}.ogg')
    sf.write(f'/tmp/{filename}.wav', data, samplerate)
    audio_file = speech_r.AudioFile(f'/tmp/{filename}.wav')
    with audio_file as source:
        audio = recogniser.record(source)
    return recogniser.recognize_google(audio, language='ru-RU')
