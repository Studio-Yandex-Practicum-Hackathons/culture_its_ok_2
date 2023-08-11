"""Основной функциол бота(просто запуск)."""
import asyncio
from aiogram import Bot, Dispatcher

from config import TELEGRAM_TOKEN
from commands import form_router


async def main():
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher()
    dp.include_router(form_router)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())
