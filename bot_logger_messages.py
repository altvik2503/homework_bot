# bot_logger_messages.py
import telegram
from typing import Union
from clever_bot import CleverBot, app_bot
import exceptions as ex
from loggers import app_logger

BOT_LOGGER_MESAGES = {
    'absent_practicum_token':
        'Отсутствует переменная окружения: токен Практикума.',
    'absent_telegram_token':
        'Отсутствует переменная окружения: токен Telegram.',
    'absent_telegram_chat_id':
        'Отсутствует переменная окружения: id чата Telegram.',
    'wrong_practicum_token':
        'Ошибочная переменная окружения: токен Практикума.',
    'wrong_telegram_token':
        'Ошибочная переменная окружения: токен Telegram.',
    'wrong_telegram_chat_id':
        'Ошибочная переменная окружения: id чата Telegram.',

    'network':
        'Ошибка сети: ',
    'end_point_status':
        'Неверный статус ответа Практикума: ',
    'end_point_connection':
        'Ошибка соединения с Практикумом: ',
    'type_homeworks': (
        'Неверный формат ответа Практикума: '
        'Тип "homeworks": ожидается "dict", получен '
    ),
    'key_homeworks': (
        'Неверный формат ответа Практикума: '
        'Отсутствует ключ "homeworks"'
    ),
    'key_homework_name': (
        'Неверный формат ответа Практикума: '
        'Отсутствует ключ "homework_name" в "homeworks.homework"'
    ),
    'key_homework_id': (
        'Неверный формат ответа Практикума: '
        'Отсутствует ключ "id" в "homeworks.homework"'
    ),
    'key_status': (
        'Неверный формат ответа Практикума: '
        'Отсутствует ключ "status" в "homeworks.homework"'
    ),
    'key_in_statuses':
        'Неверный статус домашней работы: ',

    'unhandled':
        'Сбой в работе программы: ',

    'program_abort':
        'Аварийное завершение работы программы.',
    'bot_sent':
        'Бот отправил сообщение: ',
}


def get_message_by_key(key: str) -> str:
    """Получает корректный текст сообщения."""
    return BOT_LOGGER_MESAGES.get(key, key)


# @logit
def send_memorized(
    chat_id: Union[int, str, None],
    message: object,
    is_memorized: bool = False,
    bot: CleverBot = app_bot,
) -> None:
    """Отправляет сообщение в Telegram."""
    if not bot.is_active:
        return

    str_message = str(message)

    try:
        bot.send_memorized(chat_id, str_message, is_memorized)

    except telegram.error.BadRequest as error:
        raise ex.TelegramWrongChatIdException(msg_obj=error)

    except telegram.error.Unauthorized as error:
        raise ex.TelegramWrongTokenException(msg_obj=error)

    except telegram.error.NetworkError as error:
        raise ex.TelegramNetworkErrorException(msg_obj=error)

    except Exception as error:
        raise ex.UnhandledException(msg_obj=error)

    else:
        if bot.is_sended:
            app_logger.info(f'Бот отправил сообщение: {str_message}')
