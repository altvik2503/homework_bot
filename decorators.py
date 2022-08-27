# decorators.py
import homework
import settings as stng


def logit(func):
    """Логгирует запуск и остановку функции."""
    def wrapper(*args, **kw):
        if stng.LOGIT_ON:
            msg = f'"{func.__name__}" begun.'
            homework.logit_logger.debug(msg)
        result = func(*args, **kw)
        if stng.LOGIT_ON:
            msg = f'"{func.__name__}" finished.'
            homework.logit_logger.debug(msg)
        return result
    return wrapper
