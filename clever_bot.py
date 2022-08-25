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

    _is_active: bool = False
    _is_sended: bool = False
    sended_messages: Set[str] = set()

    def __init__(self, token: str = None):
        """Инициирует бот."""
        if token:
            self.set_token(token)

    def set_token(self, token: str):
        """Назначает токен."""
        super().__init__(token)
        self._is_active = True

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

            if any([
                not is_memorized,
                memorized_key not in self.sended_messages
            ]):
                if stng.BOT_IS_ACTIVE:
                    res = super().send_message(chat_id, text, *args, **kwargs)
                self._is_sended = True
            else:
                self._is_sended = False

            if is_memorized:
                self.sended_messages.add(memorized_key)

        return res

    def send_message(self, *args, **kwargs) -> Message:
        """Отправляет сообщение, устанавливая статус отправки."""
        self._is_sended = True
        return super().send_message(*args, **kwargs)

    @property
    def is_active(self) -> bool:
        """Возвращает признак активности бота."""
        return self._is_active

    @property
    def is_sended(self) -> bool:
        """Возвращает признак отправки последнего сообщения."""
        return self._is_active


app_bot = CleverBot()
