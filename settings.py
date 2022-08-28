# settings.py
import logging
import os
from dotenv import load_dotenv

DEBUG = False

BOT_IS_ACTIVE = not DEBUG

LOGIT_ON = DEBUG

RETRY_TIME = 5 if DEBUG else 600

LOGGIN_LEVEL = logging.DEBUG if DEBUG else logging.INFO

load_dotenv()
PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN', '')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', 0)

ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
