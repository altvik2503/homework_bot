# clever_bot.py
from telegram import Message
from typing import Set, Union, Optional
from telegram import Bot
import settings as stng


class CleverBot(Bot):
    """
    Отправляет сообщение при необходимости.
    Проверяет совпадение принимающего чата и текста.
    """

    is_active: bool = False
    is_sended: bool = False
    sended_messages: Set[str] = set()

    def __init__(self, token: str = None):
        """Инициирует бот."""
        if token:
            self.set_token(token)

    def set_token(self, token: str):
        """Назначает токен."""
        super().__init__(token)
        self.is_active = True

    def get_memorized_key(
        self,
        chat_id: Optional[Union[int, str]],
        text: str
    ) -> str:
        """Создаёт форматированную уникальную строку сообщения."""
        return f'{chat_id} {text}'

    def send_memorized(
        self,
        chat_id: Optional[Union[int, str]],
        text: str,
        is_memorized: bool = True,
        *args,
        **kwargs
    ) -> Optional[Message]:
        """Отправляет сообщение, если ещё не отправлялось."""
        res = None

        if chat_id:

            memorized_key = self.get_memorized_key(chat_id, text)
            is_repeated = memorized_key in self.sended_messages

            self.is_sended = any([not is_memorized, not is_repeated])

            if all([self.is_sended, stng.BOT_IS_ACTIVE]):
                res = super().send_message(chat_id, text, *args, **kwargs)

            if all([is_memorized, not is_repeated]):
                self.sended_messages.add(memorized_key)

        return res

    def send_message(self, *args, **kwargs) -> Message:
        """Отправляет сообщение, устанавливая статус отправки."""
        self.is_sended = True
        return super().send_message(*args, **kwargs)


app_bot = CleverBot()
