"""Основной функциол бота(просто запуск)."""
import asyncio

from django.core.management.base import BaseCommand
from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramServerError

from .config import TELEGRAM_TOKEN, logger
from .commands import form_router


async def main():
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
    except TelegramServerError as error:
        logger.error(f'Ошибка в запуске бота {error}')
    dp = Dispatcher()
    dp.include_router(form_router)
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
