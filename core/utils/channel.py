from typing import Union

from aiogram import Bot
from aiogram.types import ChatMemberLeft
from config import chat_id
from core.utils.database import DbRequest


async def is_in_channel(bot: Bot, user_id: int, chat: Union[int, str]) -> bool:
    status = await bot.get_chat_member(chat, user_id)
    # print(status.status.value, type(status.status.value))
    return status.status.value != 'left'


async def num_of_valid_refs(bot: Bot, ids: list) -> int:
    cnt = 0
    for ref_id in ids:
        cnt += 1 if await is_in_channel(bot, ref_id[0], chat_id) else 0
    return cnt
