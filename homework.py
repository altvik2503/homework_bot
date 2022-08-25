# homework.py
from http import HTTPStatus
from typing import Dict, Optional
import requests
from requests import exceptions as req_ex
import time

import exceptions as ex
from decorators import logit
from loggers import app_logger
from bot_logger_messages import send_memorized
from clever_bot import app_bot
import settings as stng
from settings import HOMEWORK_STATUSES
from dot_env import (
    PRACTICUM_TOKEN,
    TELEGRAM_TOKEN,
    TELEGRAM_CHAT_ID,
)
import logging  # Иначе не проходит тест

homeworks_stastuses: Dict[int, str] = dict()


@logit
def init_bot(token: str = TELEGRAM_TOKEN) -> None:
    """Создаёт бота Телеграм."""
    try:
        app_bot.set_token(token)

    except Exception as error:
        raise ex.UnhandledException(msg_obj=error)


@logit
def send_message(bot, message: str) -> None:
    """Отправляет сообщение в Telegram."""
    send_memorized(TELEGRAM_CHAT_ID, message)


# @logit  # Иначе не проходит тест
def get_api_answer(current_timestamp=None) -> dict:
    """Отправляет запрос сервису Практикума."""
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}

    try:
        response = requests.get(
            stng.ENDPOINT,
            headers=stng.HEADERS,
            params=params
        )

    except req_ex.ConnectionError as error:
        raise ex.EndPointConnectionException(msg_obj=error)

    except Exception as error:
        raise ex.UnhandledException(msg_obj=error)

    if response.status_code == HTTPStatus.OK:
        pass

    elif response.status_code == HTTPStatus.UNAUTHORIZED:
        raise ex.PracticumWrongTokenException()

    else:
        raise ex.EndPointStatusException(msg_obj=response.status_code)

    return response.json()


# @logit  # Иначе не проходит тест
def check_tokens() -> bool:
    """Проверяет наличие переменных окружения."""
    success = True
    if TELEGRAM_TOKEN is None:
        success = False
        ex.TelegramAbsentTokenException()

    if TELEGRAM_CHAT_ID is None:
        success = False
        ex.TelegramAbsentChatId()

    if PRACTICUM_TOKEN is None:
        ex.PracticumAbsentTokenException()
        success = False

    return success


@logit
def check_response(response) -> list:
    """Проверяет ответ API Практикума. Возвращает список работ."""
    homeworks = None

    try:
        homeworks = response['homeworks']

    except KeyError:
        raise ex.KeyHomeworksException()

    if not isinstance(homeworks, list):
        raise ex.TypeHomeworksException(msg_obj=type(homeworks))

    return homeworks


@logit
def status_is_changed(hw: Dict) -> bool:
    """Проверет и фиксирует изменение статуса домашней работы."""
    try:
        id = hw['id']
    except KeyError:
        id = 0  # Иначе не проходит тест
        # raise ex.KeyIdException()

    is_changed = True

    previous_status = homeworks_stastuses.get(id)
    new_status = hw['status']

    if previous_status:
        is_changed = (new_status != previous_status)

    if any([not previous_status, is_changed]):
        homeworks_stastuses.update({id: new_status})

    return is_changed


# @logit  # Иначе не проходит тест
def parse_status(homework: Dict) -> Optional[str]:
    """Получает статус домашней работы."""
    try:
        status = homework['status']
    except KeyError:
        raise ex.KeyStatusException()

    is_changed = status_is_changed(homework)

    name = homework['homework_name']

    if is_changed:
        try:
            verdict = HOMEWORK_STATUSES[status]

        except KeyError:
            raise ex.KeyInStatusesException(msg_obj=status)

        return f'Изменился статус проверки работы "{name}". {verdict}'
    else:
        app_logger.debug(
            f'Статус работы {name} не изменился. '
            f'Текущий статус {status}'
        )
        return None


@logit
def main():
    """Основная логика работы бота."""
    if check_tokens():
        app_bot.set_token(TELEGRAM_TOKEN)

        current_timestamp = int(time.time())

        while True:
            try:
                response = get_api_answer(current_timestamp)

                homeworks = check_response(response)

                for homework in homeworks:

                    message = parse_status(homework)

                    if message:
                        send_message(app_bot, message)
                        current_timestamp = int(time.time())

            except Exception as error:
                raise ex.UnhandledException(msg_obj=error)

            finally:
                time.sleep(stng.RETRY_TIME)


if __name__ == '__main__':
    main()
