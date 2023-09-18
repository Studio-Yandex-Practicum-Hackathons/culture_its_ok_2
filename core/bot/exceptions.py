"""Кастомные исключения"""


class FeedbackError(Exception):
    """Ошибка отзыва"""
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message
