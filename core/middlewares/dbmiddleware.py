import sqlite3
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from core.utils.database import DbRequest


class DbSession(BaseMiddleware):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        with sqlite3.connect(self.connection) as connect:
            data['request'] = DbRequest(connect)
            return await handler(event, data)