"""Файл с состояниями."""

from aiogram.fsm.state import State, StatesGroup


class Route(StatesGroup):
    """Класс состояний для марштура."""
    start = State()
    choose = State()
    route = State()
    route_start = State()
    exhibit = State()
    podvodka = State()
    reflaksia = State()
    review = State()
    transition = State()
    quiz = State()
    resend_review = State()


class User(StatesGroup):
    """Класс состояний для пользователя."""
    age = State()
    name = State()
    hobby = State()


class Block(StatesGroup):
    """Класс состояний для блокировки."""
    block = State()
