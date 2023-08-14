from typing import Optional
import re

async def check_name(name: str):
    '''Проверка имени'''
    valid_pattern = re.compile(r"^[а-я,А-Я]+$", re.I)
    return bool(valid_pattern.match(name))

async def check_age(age: str):
    '''Проверка возраста'''
    if age.isnumeric():
        return int(age) > 1 and int(age) < 99
    return False

async def feedback_validator(text: str) -> Optional[str]:
    '''
    Валидация отзыва
    Возможные критерии: сообщение не пустое, в сообщение минимум N слов,
                            сообщение не может состоять только из цифр,
                            мат(если получится).
    В случае ошибки возвращаем текст
    '''
    pass

