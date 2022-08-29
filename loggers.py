# loggers.py
import logging
import logging.config
import settings as stng

logging.config.dictConfig(stng.LOGGING_CONFIG)


def get_logger(name: str) -> logging.Logger:
    """Конфигурирует логгер."""
    logger = logging.getLogger(name)
    return logger
