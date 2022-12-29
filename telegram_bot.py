# homework.py
from http import HTTPStatus
from typing import Dict, Optional
import requests
from requests import exceptions as req_ex
import time
import logging

import exceptions as ex
from clever_bot import CleverBot, app_bot
from decorators import logit
import settings as stng
from verdicts import (
    HOMEWORK_VERDICTS,
    homework_verdicts,
)
from settings import (
    PRACTICUM_TOKEN,
    TELEGRAM_TOKEN,
    TELEGRAM_CHAT_ID,
)
from loggers import get_logger


@logit
def send_message(bot: CleverBot, message: str) -> None:
    """Отправляет сообщение в Telegram."""
    bot.send_cached_message(TELEGRAM_CHAT_ID, message)


@logit
def check_tokens():
    """Проверяет наличие переменных окружения."""
    if not TELEGRAM_TOKEN:
        raise ex.TelegramAbsentTokenException

    if not TELEGRAM_CHAT_ID:
        raise ex.TelegramAbsentChatId

    if not PRACTICUM_TOKEN:
        raise ex.PracticumAbsentTokenException


@logit
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

    previous_status = homework_verdicts.get(id)

    if previous_status:
        is_changed = (new_status != previous_status)

    if any([not previous_status, is_changed]):
        homework_verdicts.update({id: new_status})

    return is_changed


@logit
def parse_status(homework: Dict) -> Optional[str]:
    """Получает статус домашней работы."""
    status = homework['status']

    try:
        verdict = HOMEWORK_VERDICTS[status]

    except KeyError:
        ex.NotKeyInStatusesException(msg_obj=status)

    name = homework['homework_name']

    id = homework['id']

    is_changed = status_is_changed(id, status)

    if is_changed:
        return f'Изменился статус проверки работы "{name}". {verdict}'
    else:
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
    test_date = stng.DEBUG_TIMESTAMP if stng.DEBUG else time.time()

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
    logger = get_logger('app_logger')

    check_tokens()

    app_bot.set_attr(token=TELEGRAM_TOKEN, logger_func=logger.info)

    current_timestamp = gеt_timestamp()

    while True:
        try:
            response = get_api_answer(current_timestamp)

            check_response_type(response)

            homeworks = check_response(response)

            for homework in homeworks:

                check_homework(homework)

                message = parse_status(homework)

                if message:
                    send_message(app_bot, message)

                    current_timestamp = gеt_timestamp()

                else:
                    logger.debug(
                        f'Статус работы {homework["homework_name"]}'
                        f' не изменился. '
                        f'Текущий статус: "{homework["status"]}"'
                    )

        except ex.ErrorLevelLogException:
            pass

        finally:
            time.sleep(stng.RETRY_TIME)


if __name__ == '__main__':
    logging.config.dictConfig(stng.LOGGING_CONFIG)

    app_logger = get_logger('app_logger')
    err_logger = get_logger('err_logger')

    try:
        app_logger.info('Запуск программы.')

        main()

    except ex.CriticalLevelLogException:
        err_logger.critical(
            'Произошла критическая ошибка. '
            'Программа остановлена.'
        )

    except Exception as err:
        err_logger.critical(
            f'Сбой в работе программы: {err}. '
            f'Аварийное завершение работы.'
        )

    except KeyboardInterrupt:
        app_logger.info('Программа остановлена пользователем.')
