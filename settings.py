# settings.py
import logging
from dot_env import PRACTICUM_TOKEN

DEBUG = True

BOT_IS_ACTIVE = not DEBUG

LOGIT_ON = True

RETRY_TIME = 10 if DEBUG else 600

LOGGIN_LEVEL = logging.DEBUG if DEBUG else logging.INFO

ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}
