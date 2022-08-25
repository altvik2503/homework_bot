# decorators.py
from loggers import logit_logger as logger
import settings as stng


def logit(func):
    """Логгирует запуск и остановку функции."""
    def wrapper(*args, **kw):
        if stng.LOGIT_ON:
            msg = f'"{func.__name__}" begun.'
            logger.debug(msg)
        result = func(*args, **kw)
        if stng.LOGIT_ON:
            msg = f'"{func.__name__}" finished.'
            logger.debug(msg)
        return result
    return wrapper
