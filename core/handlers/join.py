from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.types import ChatJoinRequest, ChatMemberUpdated

from config import chat_id
from core.utils.basic import get_link
from core.utils.database import DbRequest
from core.keyboards.basic import MainKeyboard


async def greeting(update: ChatJoinRequest, bot: Bot, request: DbRequest):
    user_info = request.get_by_id(update.from_user.id)
    if len(user_info) < 1 or user_info[0][1] == '':
        link = await get_link(bot, update.from_user.id, request,
                              update.invite_link.invite_link if update.invite_link else None)
        await bot.send_message(update.from_user.id, f'Привет, вот твоя ссылка: `{link}`',
                               parse_mode=ParseMode.MARKDOWN_V2,
                               reply_markup=MainKeyboard)
    else:
        await bot.send_message(update.from_user.id, f'Снова привет, вот твоя ссылка: `{user_info[0][1]}`',
                               parse_mode=ParseMode.MARKDOWN_V2,
                               reply_markup=MainKeyboard)
    await update.approve()


async def greeting2(update: ChatJoinRequest, bot: Bot):
    print(update)


async def joined(update: ChatMemberUpdated, bot: Bot, request: DbRequest):
    request.insert_link(update.from_user.id, '', update.invite_link.invite_link if update.invite_link else None)
