# settings.py
import os
from dotenv import load_dotenv
from datetime import datetime

DEBUG = False

BOT_IS_ACTIVE = not DEBUG

LOGIT_ON = DEBUG

RETRY_TIME = 5 if DEBUG else 600

DEBUG_TIMESTAMP = datetime(2022, 8, 20).timestamp()

# logging
LOGGIN_LEVEL = 'DEBUG' if DEBUG else 'INFO'
APP_FORMAT = '[%(asctime)s] [%(levelname)s] > %(message)s'
ERR_FORMAT = (
    '[%(asctime)s] [%(name)s] [%(levelname)s]'
    ' (%(filename)s).(%(funcName)s)(%(lineno)d) > %(message)s'
)
LOGIT_FORMAT = '[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s'
LOGGIN_DATEFMT = '%d-%b-%y %H:%M:%S'

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'app_formatter': {
            'format': APP_FORMAT,
            'datefmt': LOGGIN_DATEFMT,
        },
        'err_formatter': {
            'format': ERR_FORMAT,
            'datefmt': LOGGIN_DATEFMT,
        },
        'logit_formatter': {
            'format': LOGIT_FORMAT,
            'datefmt': LOGGIN_DATEFMT,
        },
    },

    'handlers': {
        'app_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'app_formatter',
        },
        'err_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'err_formatter',
        },
        'logit_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'logit_formatter',
        },
    },

    'loggers': {
        'app_logger': {
            'handlers': ['app_handler'],
            'level': LOGGIN_LEVEL,
            'propagate': True
        },
        'err_logger': {
            'handlers': ['err_handler'],
            'level': LOGGIN_LEVEL,
            'propagate': True
        },
        'logit_logger': {
            'handlers': ['logit_handler'],
            'level': 'DEBUG',
            'propagate': True
        },
    },
}

# environment variables
load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN', '')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', 0)

ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
