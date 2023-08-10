"""Файл с состояниями."""

from aiogram.fsm.state import State, StatesGroup


class Route(StatesGroup):
    route = State()
    exhibit = State()
    review = State()
