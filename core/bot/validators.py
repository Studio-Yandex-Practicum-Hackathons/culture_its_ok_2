import re

from bot.config import MINIMUM_WORDS_REVIEW
from bot.exceptions import FeedbackError


async def check_name(name: str) -> bool:
    """Проверка имени"""
    valid_pattern = re.compile(r"^[а-я,А-Я]+$", re.I)
    return bool(valid_pattern.match(name))


async def check_age(age: str) -> bool:
    """Проверка возраста"""
    if age.isnumeric():
        return int(age) > 1 and int(age) < 99
    return False


async def rewiew_validator(text: str) -> None:
    """
    Валидация отзыва

    Возможные критерии: сообщение не пустое, в сообщение минимум N слов,
                            сообщение не может состоять только из цифр,
                            мат(если получится).
    """
    if (not text
            or text.count(" ") < MINIMUM_WORDS_REVIEW - 1
            or text.isdigit()):
        raise FeedbackError(
            "Получен пустой отзыв, или в отзыве менее трёх слов, "
            "или отзыв состоит только из цифр"
        )
