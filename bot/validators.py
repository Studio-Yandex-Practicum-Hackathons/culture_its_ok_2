from exceptions import FeedbackError


async def feedback_validator(text: str) -> None:
    '''
    Валидация отзыва

    Возможные критерии: сообщение не пустое, в сообщение минимум N слов,
                            сообщение не может состоять только из цифр,
                            мат(если получится).
    '''
    if not text or text.count(' ') < 2 or text.isdigit():
        raise FeedbackError(
            'Получен пустой отзыв, или в отзыве менее трёх слов, '
            'или отзыв состоит только из цифр'
        )
