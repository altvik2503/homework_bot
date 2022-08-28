# exceptions.py
from typing import Callable
import homework
from settings import TELEGRAM_CHAT_ID

BOT_LOGGER_MESAGES = {
    # Ошибки переменных окружения
    'absent_practicum_token':
        'Отсутствует переменная окружения: токен Практикума.',
    'absent_telegram_token':
        'Отсутствует переменная окружения: токен Telegram.',
    'absent_telegram_chat_id':
        'Отсутствует переменная окружения: id чата Telegram.',
    'wrong_practicum_token':
        'Ошибочная переменная окружения: токен Практикума: ',
    'wrong_telegram_token':
        'Ошибочная переменная окружения: токен Telegram: ',
    'wrong_telegram_chat_id':
        'Ошибочная переменная окружения: id чата Telegram: ',
    # Ошибки Практикума
    'connection':
        'Ошибка соединения с Практикумом: ',
    'request':
        'Ошибка запроса Практикума: ',
    'not_found':
        'Запрашиваемая страница не найдена: ',
    'end_point_status':
        'Неверный статус ответа Практикума: ',
    # Ошибки формата ответа Практикума
    'type_response': (
        'Неверный формат ответа Практикума: '
        'Тип "response": ожидается "dict", получен '
    ),
    'type_homeworks': (
        'Неверный формат ответа Практикума: '
        'Тип "homeworks": ожидается "dict", получен '
    ),
    'key_homeworks': (
        'Неверный формат ответа Практикума: '
        'Отсутствует ключ "homeworks".'
    ),
    'key_homework_name': (
        'Неверный формат ответа Практикума: '
        'Отсутствует ключ "homework_name".'
    ),
    'key_homework_id': (
        'Неверный формат ответа Практикума: '
        'Отсутствует ключ "id".'
    ),
    'key_status': (
        'Неверный формат ответа Практикума: '
        'Отсутствует ключ "status"'
    ),
    'key_in_statuses':
        'Неверный статус домашней работы: ',
    # Прочие ошибки
    'network':
        'Ошибка сети: ',
}


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
        self.message = BOT_LOGGER_MESAGES.get(key, key)
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


class CriticalLevelNotBotException(CriticalLevelLogException):
    """Обрабатывает критические ошибки."""

    def __init__(self, *args, **kwargs) -> None:
        """Инициирует объект с уровнем CRITICAL."""
        super().__init__(*args, is_send_message=False, **kwargs)


class ErrorLevelNotBotException(ErrorLevelLogException):
    """Обрабатывает ошибки уровня ERROR."""

    def __init__(self, *args, **kwargs) -> None:
        """Инициирует объект с уровнем ERROR."""
        super().__init__(*args, is_send_message=False, **kwargs)


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


class TelegramAbsentTokenException(CriticalLevelNotBotException):
    """Отсутствует токен Телеграм."""

    def __init__(self, *args, **kwargs) -> None:
        """Обработка ошибки отсутствия токена Телеграм."""
        super().__init__('absent_telegram_token', *args, **kwargs)


class TelegramAbsentChatId(CriticalLevelNotBotException):
    """Отсутствует ID чата Телеграм."""

    def __init__(self, *args, **kwargs) -> None:
        """Обработка ошибки отсутствия ID чата Телеграм."""
        super().__init__('absent_telegram_chat_id', *args, **kwargs)


class TelegramWrongTokenException(CriticalLevelNotBotException):
    """Некорректный токен Телеграм."""

    def __init__(self, *args, **kwargs) -> None:
        """Обработка ошибки некорректного токена Телеграм."""
        super().__init__('wrong_telegram_token', *args, **kwargs)


class TelegramWrongChatIdException(CriticalLevelNotBotException):
    """Некорректный ID чата Телеграм."""

    def __init__(self, *args, **kwargs) -> None:
        """Обработка ошибки некорректного ID чата Телеграм."""
        super().__init__('wrong_telegram_chat_id', *args, **kwargs)


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


# Ошибки Телеграм``
class TelegramNetworkErrorException(ErrorLevelNotBotException):
    """Ошибка сети Телеграм."""

    def __init__(self, *args, **kwargs) -> None:
        """Обработка ошибки сети Телеграм."""
        super().__init__('network', *args, **kwargs)


class TelegramUnhandledException(ErrorLevelNotBotException):
    """Ошибка при работе Телеграм."""

    def __init__(self, *args, **kwargs) -> None:
        """Обработка ошибки работы Телеграм."""
        super().__init__('telegram', *args, **kwargs)
