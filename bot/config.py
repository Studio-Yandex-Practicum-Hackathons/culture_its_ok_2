"""Настройки бота и прочее."""
import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

MINIMUM_WORDS_REVIEW: int = 3
SUCCESSFUL_MESSAGE: str = 'Спасибо за отзыв.'
