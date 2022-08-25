# loggers.py
import logging
import sys
import settings as stng

BASE_LOGGER_NAME = __name__

logging.basicConfig(
    level=stng.LOGGIN_LEVEL,
    stream=sys.stdout,
    format='[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s'
)
app_logger = logging.getLogger(BASE_LOGGER_NAME)
logit_logger = logging.getLogger(f'{BASE_LOGGER_NAME}.logit')
exception_logger = logging.getLogger(f'{BASE_LOGGER_NAME}.err')
