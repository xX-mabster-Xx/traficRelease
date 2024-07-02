from aiogram import Bot

from config import chat_id, bot_name, join_request
from core.utils.channel import num_of_valid_refs, is_in_channel

from core.utils.database import DbRequest
from logger import logger


async def get_link(bot: Bot, user_id, request: DbRequest, invited_by=None):
    info = request.get_by_id(user_id)
    if len(info) > 0 and len(info[0][1]) > 1:
        return info[0][1]
    try:
        result = await bot.create_chat_invite_link(chat_id, f'U{user_id}',
                                                   creates_join_request=join_request)
    except Exception as e:
        logger.error(e)
        return f'https://t.me/{bot_name[1:]}?start={user_id}'
    else:
        if len(info) > 0:
            request.edit_link(user_id, result.invite_link)
        else:
            request.insert_link(user_id, result.invite_link, invited_by)
        return result.invite_link


async def count_weight(bot: Bot, user_id: int, request: DbRequest):
    if not await is_in_channel(bot, user_id, chat_id):
        return 0
    return 1 + 0.2 * (await num_of_valid_refs(bot, request.get_refs(user_id)))
