# clever_bot.py
from telegram import Message, error as bot_err, Bot
from typing import Callable, Set, Union, Optional

import exceptions as ex
import settings as stng


class CleverBot(Bot):
    """
    Кэширует отправляемые сообщения.
    Отправляет сообщение при необходимости.
    Логгирует факт отправки сообщения.
    """

    def __init__(
        self,
        token: str = None,
        logger_func: Callable = None
    ) -> None:
        """Инициирует бот."""
        self.is_active: bool = False
        self.cached_messages: Set[str] = set()
        self.logger_func: Callable = None
        if token:
            self.set_attr(token, logger_func)

    def set_attr(self, token: str = '', logger_func: Callable = None) -> None:
        """Назначает аттрибуты."""
        self.logger_func = logger_func
        if token:
            super().__init__(token)
            self.is_active = True

    def get_memorized_key(self, chat_id: Union[int, str], text: str) -> str:
        """Создаёт уникальную строку сообщения для кэширования."""
        return f'{chat_id} {text}'

    def send_cached_message(
        self,
        chat_id: Union[int, str],
        text: str,
        *args,
        do_not_repeat: bool = False,
        **kwargs,
    ) -> Optional[Message]:
        """Кэширует, отправляет и логгирует сообщение."""
        to_send = True

        if do_not_repeat:

            memorized_key = self.get_memorized_key(chat_id, text)

            to_send = memorized_key not in self.cached_messages

            self.cached_messages.add(memorized_key)

        res = None

        if to_send:
            if stng.BOT_IS_ACTIVE:
                try:
                    res = super().send_message(chat_id, text, *args, **kwargs)
                except bot_err.BadRequest as error:
                    raise ex.TelegramWrongChatIdException(msg_obj=error)

                except bot_err.Unauthorized as error:
                    raise ex.TelegramWrongTokenException(msg_obj=error)

                except bot_err.NetworkError as error:
                    raise ex.TelegramNetworkErrorException(msg_obj=error)

                except Exception as error:
                    raise ex.TelegramUnhandledException(msg_obj=error)

            if self.logger_func:
                self.logger_func(f'Бот отправил сообщение: {text}')

        return res


app_bot = CleverBot()
