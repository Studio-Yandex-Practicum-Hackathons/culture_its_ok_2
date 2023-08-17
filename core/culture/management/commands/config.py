"""Настройки бота и прочее."""
import os
import logging

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

ADMIN_ID = os.getenv('ADMIN_ID')
BASE_DIR = os.getenv('BASE_DIR')


MINIMUM_WORDS_REVIEW: int = 3

logging.basicConfig(
    handlers=[logging.FileHandler(
        filename="main.log",
        encoding='utf-8', mode='w')],
    format='%(asctime)s, %(levelname)s, %(message)s',
    level=logging.DEBUG,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler(
    'Bot.log',
    maxBytes=50000000,
    backupCount=5,
    encoding='utf-8',
)
formatter = logging.Formatter('%(asctime)s, %(levelname)s, %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


if TELEGRAM_TOKEN is None:
    logger.critical('Нет TELEGRAM_TOKEN.')
