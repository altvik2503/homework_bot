# exceptions.py
from typing import Callable
import bot_logger_messages
import homework
from settings import TELEGRAM_CHAT_ID


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
        self.message = bot_logger_messages.get_message_by_key(key)
        if msg_obj:
            self.message += str(msg_obj)

        logger_fun(self.message)

        if is_send_message:
            homework.send_memorized(
                TELEGRAM_CHAT_ID,
                self.message,
                is_memorized=True
            )

    def __str__(self) -> str:
        """Возвращает текст сообщения."""
        return self.message


class CriticalLevelLogException(LoggedException):
    """Обрабатывает критические ошибки."""

    def __init__(self, key: str, *args, **kwargs) -> None:
        """Инициирует объект с уровнем CRITICAL."""
        super().__init__(
            key,
            homework.exception_logger.critical,
            *args,
            **kwargs
        )


class ErrorLevelLogException(LoggedException):
    """Обрабатывает ошибки уровня ERROR."""

    def __init__(self, key: str, *args, **kwargs) -> None:
        """Инициирует объект с уровнем ERROR."""
        super().__init__(
            key,
            homework.exception_logger.error,
            *args,
            **kwargs
        )


# Ошибки переменных окружения
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
        super().__init__(
            'absent_telegram_token',
            *args,
            is_send_message=False,
            **kwargs,
        )


class TelegramAbsentChatId(CriticalLevelLogException):
    """Отсутствует ID чата Телеграм."""

    def __init__(self, *args, **kwargs) -> None:
        """Обработка ошибки отсутствия ID чата Телеграм."""
        super().__init__(
            'absent_telegram_chat_id',
            *args,
            is_send_message=False,
            **kwargs,
        )


class TelegramWrongTokenException(CriticalLevelLogException):
    """Некорректный токен Телеграм."""

    def __init__(self, *args, **kwargs) -> None:
        """Обработка ошибки некорректного токена Телеграм."""
        super().__init__(
            'wrong_telegram_token',
            *args,
            is_send_message=False,
            **kwargs,
        )


class TelegramWrongChatIdException(CriticalLevelLogException):
    """Некорректный ID чата Телеграм."""

    def __init__(self, *args, **kwargs) -> None:
        """Обработка ошибки некорректного ID чата Телеграм."""
        super().__init__(
            'wrong_telegram_chat_id',
            *args,
            is_send_message=False,
            **kwargs,
        )


# Ошибки Практикума
class ConnectionException(ErrorLevelLogException):
    """Ошибка соединения с Практикумом."""

    def __init__(self, *args, **kwargs) -> None:
        """Обработка ошибки соединения с Практикумом."""
        super().__init__('connection', *args, **kwargs)


class RequestException(ErrorLevelLogException):
    """Прочая ошибка запроса Практикума."""

    def __init__(self, *args, **kwargs) -> None:
        """Обработка прочей ошибки запроса  Практикума."""
        super().__init__('request', *args, **kwargs)


class NotFoundException(ErrorLevelLogException):
    """Страница не найдена."""

    def __init__(self, *args, **kwargs) -> None:
        """Обработка ошибки ненайденной страницы."""
        super().__init__('not_found', *args, **kwargs)


class EndPointStatusException(ErrorLevelLogException):
    """Неверный статус ответа от Практикума."""

    def __init__(self, *args, **kwargs) -> None:
        """Обработка ошибки неверного статуса ответа от Практикума."""
        super().__init__('end_point_status', *args, **kwargs)


# Ошибки формата ответа Практикума
class ResponseNotDictException(ErrorLevelLogException):
    """Неверный тип response."""

    def __init__(self, *args, **kwargs) -> None:
        """Обработка неверного тип response."""
        super().__init__('type_response', *args, **kwargs)


class HomeworksNotListException(ErrorLevelLogException):
    """Неверный тип ключа 'homeworks'."""

    def __init__(self, *args, **kwargs) -> None:
        """Обработка ошибки неверного типа ключа 'homeworks'."""
        super().__init__('type_homeworks', *args, **kwargs)


class NotKeyHomeworksException(ErrorLevelLogException):
    """Отсутствие ключа 'homeworks'."""

    def __init__(self, *args, **kwargs) -> None:
        """Обработка ошибки отсутствия ключа 'homeworks'."""
        super().__init__('key_homeworks', *args, **kwargs)


class NotKeyNameException(ErrorLevelLogException):
    """Отсутствие ключа 'homework_name'."""

    def __init__(self, *args, **kwargs) -> None:
        """Обработка ошибки отсутствия ключа 'homework_name'."""
        super().__init__('key_homework_name', *args, **kwargs)


class NotKeyIdException(ErrorLevelLogException):
    """Отсутствие ключа 'id'."""

    def __init__(self, *args, **kwargs) -> None:
        """Обработка ошибки отсутствия ключа 'id'."""
        super().__init__('key_homework_id', *args, **kwargs)


class NotKeyStatusException(ErrorLevelLogException):
    """Отсутствие ключа 'key_status'."""

    def __init__(self, *args, **kwargs) -> None:
        """Обработка ошибки отсутствия ключа 'key_status'."""
        super().__init__('key_status', *args, **kwargs)


class NotKeyInStatusesException(ErrorLevelLogException):
    """Неверный тип ключа 'status'."""

    def __init__(self, *args, **kwargs) -> None:
        """Обработка ошибки неверного типа ключа 'status'."""
        super().__init__('key_in_statuses', *args, **kwargs)


# Прочие ошибки
class TelegramNetworkErrorException(ErrorLevelLogException):
    """Ошибка сети Телеграм."""

    def __init__(self, *args, **kwargs) -> None:
        """Обработка ошибки сети Телеграм."""
        super().__init__('network', *args, **kwargs)


class TelegramUnhandledException(ErrorLevelLogException):
    """Ошибка при работе Телеграм."""

    def __init__(self, *args, **kwargs) -> None:
        """Обработка ошибки работы Телеграм."""
        super().__init__('telegram', *args, **kwargs)
