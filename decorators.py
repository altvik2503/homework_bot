# decorators.py
from time import time
from loggers import get_logger
from settings import LOGIT_ON

logit_logger = get_logger('logit_logger')


def logit(func):
    """
    Логгирует запуск и остановку функции.
    Измеряет время выполненния функции.
    """
    def wrapper(*args, **kw):
        if LOGIT_ON:
            msg = f'"{func.__name__}" стартовал.'
            logit_logger.debug(msg)
            start_time = time()
        result = func(*args, **kw)
        if LOGIT_ON:
            msg = (
                f'"{func.__name__}" финишировал. '
                f'Время работы: {(time()-start_time)/1000:.3f} миллисекунд.'
            )
            logit_logger.debug(msg)
        return result
    return wrapper
