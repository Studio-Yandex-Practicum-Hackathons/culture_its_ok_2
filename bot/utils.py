"""Файл с состояниями."""

from aiogram.fsm.state import State, StatesGroup


class Route(StatesGroup):
    """Класс состояний для марштура."""
    route = State()
    exhibit = State()
    review = State()
    transition = State()
    quiz = State()


class User(StatesGroup):
    """Класс состояний для пользователя."""
    name = State()
    age = State()
    hobby = State()
