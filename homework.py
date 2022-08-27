# homework.py
from http import HTTPStatus
from typing import Dict, Optional, Union
import requests
from requests import exceptions as req_ex
from datetime import datetime
import time
import telegram
import sys
import logging

import exceptions as ex
from clever_bot import CleverBot
from decorators import logit
import settings as stng
from statuses import (
    HOMEWORK_STATUSES,
    homeworks_statuses,
)
from settings import (
    PRACTICUM_TOKEN,
    TELEGRAM_TOKEN,
    TELEGRAM_CHAT_ID,
)

BASE_LOGGER_NAME = __name__

logging.basicConfig(
    level=stng.LOGGIN_LEVEL,
    stream=sys.stdout,
    format='[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
)
app_logger = logging.getLogger(BASE_LOGGER_NAME)
logit_logger = logging.getLogger(f'{BASE_LOGGER_NAME}.logit')
exception_logger = logging.getLogger(f'{BASE_LOGGER_NAME}.err')

app_bot = CleverBot()


@logit
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

    except telegram.error.Unauthorized:
        raise ex.TelegramWrongTokenException

    except telegram.error.NetworkError as error:
        raise ex.TelegramNetworkErrorException(msg_obj=error)

    except Exception as error:
        raise ex.TelegramUnhandledException(msg_obj=error)

    else:
        if bot.is_sended:
            app_logger.info(f'Бот отправил сообщение: {str_message}')


@logit
def send_message(bot: CleverBot, message: str) -> None:
    """Отправляет сообщение в Telegram."""
    send_memorized(TELEGRAM_CHAT_ID, message, bot=bot)


# @logit  # Иначе не проходит тест
def check_tokens() -> bool:
    """Проверяет наличие переменных окружения."""
    is_success = True

    if TELEGRAM_TOKEN is None:
        is_success = False
        ex.TelegramAbsentTokenException()

    if TELEGRAM_CHAT_ID is None:
        is_success = False
        ex.TelegramAbsentChatId()

    if PRACTICUM_TOKEN is None:
        is_success = False
        ex.PracticumAbsentTokenException()

    return is_success


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
        raise ex.ConnectionException(msg_obj=error)

    except Exception as error:
        raise ex.RequestException(msg_obj=error)

    if response.status_code == HTTPStatus.OK:
        pass

    elif response.status_code == HTTPStatus.NOT_FOUND:
        raise ex.NotFoundException(msg_obj=stng.ENDPOINT)

    elif response.status_code == HTTPStatus.UNAUTHORIZED:
        raise ex.PracticumWrongTokenException()

    else:
        raise ex.EndPointStatusException(msg_obj=response.status_code)

    return response.json()


@logit
def check_response(response) -> list:
    """Проверяет ответ API Практикума. Возвращает список работ."""
    homeworks = None

    try:
        homeworks = response['homeworks']

    except KeyError:
        raise ex.NotKeyHomeworksException()

    if not isinstance(homeworks, list):
        raise ex.HomeworksNotListException(msg_obj=type(homeworks))

    return homeworks


@logit
def status_is_changed(id: int, new_status: str) -> bool:
    """Проверет и фиксирует изменение статуса домашней работы."""
    is_changed = True

    previous_status = homeworks_statuses.get(id)

    if previous_status:
        is_changed = (new_status != previous_status)

    if any([not previous_status, is_changed]):
        homeworks_statuses.update({id: new_status})

    return is_changed


# @logit  # Иначе не проходит тест
def parse_status(homework: Dict) -> Optional[str]:
    """Получает статус домашней работы."""
    status = homework['status']

    try:
        verdict = HOMEWORK_STATUSES[status]

    except KeyError:
        ex.NotKeyInStatusesException(msg_obj=status)

    name = homework['homework_name']

    id = homework['id']

    is_changed = status_is_changed(id, status)

    if is_changed:
        return f'Изменился статус проверки работы "{name}". {verdict}'
    else:
        app_logger.debug(
            f'Статус работы {name} не изменился. '
            f'Текущий статус: "{status}"'
        )
        return None


@logit
def check_homework(homework: Dict) -> None:
    """Проверяет корректность формата полученной homework."""
    try:
        _ = homework['homework_name']
    except KeyError:
        raise ex.NotKeyNameException

    try:
        _ = homework['id']
    except KeyError:
        raise ex.NotKeyIdException

    try:
        _ = homework['status']
    except KeyError:
        raise ex.NotKeyStatusException


@logit
def gеt_timestamp() -> int:
    """Формирует время запроса к Практикуму."""
    if stng.DEBUG:
        test_date = datetime(2022, 7, 30).timestamp()
    else:
        test_date = time.time()

    return int(test_date)


@logit
def check_response_type(response: object) -> None:
    """Проверяет тип данных ответа Практикума."""
    if not isinstance(response, dict):
        raise ex.ResponseNotDictException(
            msg_obj=type(response)
        )


@logit
def main():
    """Основная логика работы бота."""
    if not check_tokens():
        return

    app_bot.set_token(TELEGRAM_TOKEN)

    current_timestamp = gеt_timestamp()

    is_running = True

    while is_running:
        try:
            response = get_api_answer(current_timestamp)

            check_response_type(response)

            homeworks = check_response(response)

            for homework in homeworks:

                check_homework(homework)

                message = parse_status(homework)

                if message:
                    send_message(app_bot, message)

                    if not stng.DEBUG:
                        current_timestamp = gеt_timestamp()

        except ex.ErrorLevelLogException:
            pass

        except ex.CriticalLevelLogException:
            app_logger.critical(
                'Произошла критическая ошибка. Программа остановлена.'
            )
            is_running = False

        except Exception as err:
            app_logger.critical(
                f'Сбой в работе программы: {err}. '
                f'Аварийное завершение работы.'
            )
            is_running = False

        finally:
            if is_running:
                time.sleep(stng.RETRY_TIME)


if __name__ == '__main__':
    main()
