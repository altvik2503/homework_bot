# clever_bot.py
from telegram import Message, error as bot_err, Bot
from typing import Set, Union, Optional

import exceptions as ex
import settings as stng


class CleverBot(Bot):
    """
    Кэширует отправляемые сообщения.
    Отправляет сообщение при необходимости.
    """

    def __init__(self, token: str = None):
        """Инициирует бот."""
        self.is_active: bool = False
        self.is_sended: bool = False
        self.sended_messages: Set[str] = set()
        if token:
            self.set_token(token)

    def set_token(self, token: str):
        """Назначает токен."""
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
        not_repeat: bool = False,
        **kwargs,
    ) -> Optional[Message]:
        """Отправляет сообщение, устанавливая статус отправки."""
        self.is_sended = True

        if not_repeat:

            memorized_key = self.get_memorized_key(chat_id, text)

            self.is_sended = memorized_key not in self.sended_messages

            self.sended_messages.add(memorized_key)

        if all([self.is_sended, stng.BOT_IS_ACTIVE]):
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
        else:
            res = None

        return res


app_bot = CleverBot()
