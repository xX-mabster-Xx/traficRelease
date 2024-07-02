from aiogram import types
from aiogram.filters import Filter
from aiogram.types import Message, ChatJoinRequest


class MyFilter(Filter):
    def __init__(self, chat_id: str) -> None:
        self.my_text = chat_id

    async def __call__(self, update: ChatJoinRequest) -> bool:
        return update.chat.id == self.my_text