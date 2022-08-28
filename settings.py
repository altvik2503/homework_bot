# settings.py
import logging
import os
from dotenv import load_dotenv

DEBUG = True

BOT_IS_ACTIVE = DEBUG

LOGIT_ON = not DEBUG

RETRY_TIME = 5 if DEBUG else 600

LOGGIN_LEVEL = logging.DEBUG if DEBUG else logging.INFO

load_dotenv()
PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
