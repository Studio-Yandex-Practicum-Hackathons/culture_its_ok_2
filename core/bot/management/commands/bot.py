import asyncio
from typing import Any, Optional

from django.core.management.base import BaseCommand

from bot.bot import main
from bot.config import logger


class Command(BaseCommand):
    help = "Запускает бота."

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        try:
            asyncio.run(main())
        except (KeyboardInterrupt, SystemExit):
            logger.info("Bot stopped")
