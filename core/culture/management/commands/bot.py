"""Основной функциол бота(просто запуск)."""
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramServerError
from django.core.management.base import BaseCommand

from .commands import main_router
from .config import TELEGRAM_TOKEN, logger


async def main():
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
    except TelegramServerError as error:
        logger.error(f'Ошибка в запуске бота {error}')
    dp = Dispatcher()
    dp.include_router(main_router)
    # не уверен что надо иммено тут
    logger.info("Bot включился!")

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


class Command(BaseCommand):
    help = 'Implemented to Django application telegram bot setup command'

    def handle(self, *args, **kwargs):
        try:
            asyncio.run(main())
        except (KeyboardInterrupt, SystemExit):
            logger.info("Bot stopped!")
