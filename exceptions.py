# exceptions.py
from loggers import exception_logger as logger
from typing import Callable

from bot_logger_messages import get_message_by_key
from bot_logger_messages import send_memorized
from dot_env import TELEGRAM_CHAT_ID


class LoggedException(Exception):
    """Логгирует ошибку и отправляет сообщение в Телеграм."""

    message: str = ''

    def __init__(
        self,
        key: str,
        logger_fun: Callable,
        msg_obj: object = None,
        is_send_message: bool = True,
    ) -> None:
        """Логгирует ошибку, отправляет сообщение в Телеграмм."""
        self.message = get_message_by_key(key)
        if msg_obj:
            self.message += str(msg_obj)

        logger_fun(self.message)

        if is_send_message:
            send_memorized(TELEGRAM_CHAT_ID, self.message, is_memorized=True)

    def __str__(self) -> str:
        """Возвращает текст сообщения."""
        return self.message


class CriticalLevelLogException(LoggedException):
    """Обрабатывает критические ошибки."""

    def __init__(self, key: str, *args, **kwargs) -> None:
        """Инициирует объект с уровнем CRITICAL."""
        super().__init__(key, logger.critical, *args, **kwargs)

        logger.critical(get_message_by_key('program_abort'))


class ErrorLevelLogException(LoggedException):
    """Обрабатывает ошибки уровня ERROR."""

    def __init__(self, key: str, *args, **kwargs) -> None:
        """Инициирует объект с уровнем ERROR."""
        super().__init__(key, logger.error, *args, **kwargs)


class NotMessageErrorLogException(ErrorLevelLogException):
    """
    Обрабатывает ошибки уровня ERROR.
    Не посылает сообщения в Телеграм.
    """

    def __init__(self, key: str, *args, **kwargs) -> None:
        """Инициирует объект с уровнем ERROR."""
        super().__init__(
            key,
            logger.error,
            *args,
            is_send_message=False,
            **kwargs
        )


class PracticumAbsentTokenException(CriticalLevelLogException):
    """Отсутствует токен Телеграм."""

    def __init__(self, *args, **kwargs) -> None:
        """Обработка ошибки отсутствия токена Телеграм."""
        super().__init__('absent_practicum_token', *args, **kwargs)


class PracticumWrongTokenException(CriticalLevelLogException):
    """Некорректный токен Практикума."""

    def __init__(self, *args, **kwargs) -> None:
        """Обработка ошибки некорректного токена Практикума."""
        super().__init__('wrong_practicum_token', *args, **kwargs)


class TelegramAbsentTokenException(CriticalLevelLogException):
    """Отсутствует токен Телеграм."""

    def __init__(self, *args, **kwargs) -> None:
        """Обработка ошибки отсутствия токена Телеграм."""
        super().__init__('absent_telegram_token', *args, **kwargs)


class TelegramAbsentChatId(CriticalLevelLogException):
    """Отсутствует ID чата Телеграм."""

    def __init__(self, *args, **kwargs) -> None:
        """Обработка ошибки отсутствия ID чата Телеграм."""
        super().__init__('absent_telegram_chat_id', *args, **kwargs)


class TelegramWrongTokenException(CriticalLevelLogException):
    """Некорректный токен Телеграм."""

    def __init__(self, *args, **kwargs) -> None:
        """Обработка ошибки некорректного токена Телеграм."""
        super().__init__('wrong_telegram_token', *args, **kwargs)


class TelegramWrongChatIdException(CriticalLevelLogException):
    """Некорректный ID чата Телеграм."""

    def __init__(self, *args, **kwargs) -> None:
        """Обработка ошибки некорректного ID чата Телеграм."""
        super().__init__('wrong_telegram_chat_id', *args, **kwargs)


class TelegramNetworkErrorException(NotMessageErrorLogException):
    """Ошибка сети."""

    def __init__(self, *args, **kwargs) -> None:
        """Обработка ошибки сети."""
        super().__init__('network', *args, **kwargs)


class EndPointStatusException(ErrorLevelLogException):
    """Неверный код ответа от Практикума."""

    def __init__(self, *args, **kwargs) -> None:
        """Обработка ошибки неверного код ответа от Практикума."""
        super().__init__('end_point_status', *args, **kwargs)


class EndPointConnectionException(NotMessageErrorLogException):
    """Ошибка соединения с Практикумом."""

    def __init__(self, *args, **kwargs) -> None:
        """Обработка ошибки соединения с Практикумом."""
        super().__init__('end_point_connection', *args, **kwargs)


class TypeHomeworksException(ErrorLevelLogException):
    """Неверный тип ключа 'homeworks'."""

    def __init__(self, *args, **kwargs) -> None:
        """Обработка ошибки неверного типа ключа 'homeworks'."""
        super().__init__('type_homeworks', *args, **kwargs)


class KeyHomeworksException(ErrorLevelLogException):
    """Отсутствие ключа 'homeworks'."""

    def __init__(self, *args, **kwargs) -> None:
        """Обработка ошибки отсутствия ключа 'homeworks'."""
        super().__init__('key_homeworks', *args, **kwargs)


class KeyHomeworkException(ErrorLevelLogException):
    """Отсутствие ключа 'homework_name'."""

    def __init__(self, *args, **kwargs) -> None:
        """Обработка ошибки отсутствия ключа 'homework_name'."""
        super().__init__('key_homework_name', *args, **kwargs)


class KeyIdException(ErrorLevelLogException):
    """Отсутствие ключа 'id'."""

    def __init__(self, *args, **kwargs) -> None:
        """Обработка ошибки отсутствия ключа 'id'."""
        super().__init__('key_homework_id', *args, **kwargs)


class KeyStatusException(ErrorLevelLogException):
    """Отсутствие ключа 'key_status'."""

    def __init__(self, *args, **kwargs) -> None:
        """Обработка ошибки отсутствия ключа 'key_status'."""
        super().__init__('key_status', *args, **kwargs)


class KeyInStatusesException(ErrorLevelLogException):
    """Неверный тип ключа 'status'."""

    def __init__(self, *args, **kwargs) -> None:
        """Обработка ошибки неверного типа ключа 'status'."""
        super().__init__('key_in_statuses', *args, **kwargs)


class UnhandledException(CriticalLevelLogException):
    """Необработанная ошибка."""

    def __init__(self, *args, **kwargs) -> None:
        """Обработка необработанной ошибки."""
        super().__init__('unhandled', *args, **kwargs)
