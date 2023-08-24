"""Основной функциол бота(просто запуск)."""

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramServerError

from .commands import main_router
from .config import TELEGRAM_TOKEN, logger


async def main():
    try:
        bot = Bot(token=TELEGRAM_TOKEN, parse_mode='html')
    except TelegramServerError as error:
        logger.error(f"Ошибка в запуске бота {error}")
    dp = Dispatcher()
    dp.include_router(main_router)
    logger.info("Bot включился!")

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
