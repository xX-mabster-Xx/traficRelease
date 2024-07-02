import hashlib

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.types import Message, ChatJoinRequest, InlineQuery, InlineQueryResultArticle, InputTextMessageContent

from config import chat_id, main_link, bot_name, join_request
from core.keyboards.basic import MainKeyboard
from core.utils.basic import get_link, count_weight
from core.utils.channel import is_in_channel
from core.utils.database import DbRequest
from logger import logger


async def startbot(bot: Bot):

    pass
    # 350877911
    # print(await is_in_channel(bot, 887, chat_id))
    # await bot.revoke_chat_invite_link(chat_id=chat_id, invite_link='https://t.me/')
    # await bot.create_chat_invite_link(chat_id, f'MAIN',
    #                                   creates_join_request=join_request)


async def update_pool_info(message: Message, bot: Bot, request: DbRequest):
    users = request.get_users()
    total = 0
    for user in users:
        total += await count_weight(bot, user[0], request)
        # print(user, await count_weight(bot, user[0], request))
    await message.answer(f"Total weight: {total}")
    if len(message.text.split()) > 1 and message.text.split()[1].isnumeric():
        request.insert_pool_info(total, int(message.text.split()[1]))
    else:
        request.insert_pool_info(total, request.get_pool_info()[1])


async def get_start(message: Message, bot: Bot, request: DbRequest):
    info = request.get_by_id(message.from_user.id)
    if len(info) > 0 or await is_in_channel(bot, message.from_user.id, chat_id):
        link = await get_link(bot, message.from_user.id, request)
        text = (f'Привет,\n'
                f'Вот твоя ссылка: `{link}`')
        await bot.send_message(message.chat.id, text, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=MainKeyboard)
    elif len(message.text.split()) > 1 and message.text.split()[1].isnumeric() and \
            (len(request.get_by_id(int(message.text.split()[1]))) > 0 or
             await is_in_channel(bot, int(message.text.split()[1]), chat_id)):
        print('sigma zashla', message.text.split()[1])
        request.insert_link(message.from_user.id, '', int(message.text.split()[1]))
        text = (f'Привет,\n'
                f'Для началa вы должны присоединиться к [каналу]({main_link})')
        await bot.send_message(message.chat.id, text, parse_mode=ParseMode.MARKDOWN_V2)
    else:
        text = (f'Привет,\n'
                f'Для началa вы должны присоединиться к [каналу]({main_link})')
        await bot.send_message(message.chat.id, text, parse_mode=ParseMode.MARKDOWN_V2)


async def print_message(message: Message, bot: Bot):
    if message.dice:
        await bot.send_message(message.from_user.id, f'{message.dice.emoji}:{message.dice.value}')
    else:
        pass



async def inline_handler(query: InlineQuery, bot: Bot):
    print(query)
    result_id = hashlib.md5(query.query.encode()).hexdigest()
    articles = [ InlineQueryResultArticle(id=result_id,
                                          title="LOLOLO",
                                          input_message_content=InputTextMessageContent(message_text="penis"))]
    await query.answer(articles, cache_time=1, is_personal=True)






async def handler(update, bot: Bot):
    print(update)
    await bot.send_message(chat_id=update.from_user.id, text="lololo")


# async def get_links(message: Message, bot: Bot, request: DbRequest):
#     info = request.get_by_id(message.from_user.id)
#     if len(info) > 0:
#         text = (f'Вот твоя ссылка: `{info[0][1]}`\n'
#                 f'айа: 220')
#         await bot.send_message(message.chat.id, text, parse_mode=ParseMode.MARKDOWN_V2)
#     else:
#         text = (f'Привет,\n'
#                 f'Для начал вы должны присоединиться к [каналу]({main_link})')
#         await bot.send_message(message.chat.id, text, parse_mode=ParseMode.MARKDOWN_V2)
