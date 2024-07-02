import asyncio
import json

from aiogram import Bot, Dispatcher, F
from aiogram.handlers import CallbackQueryHandler
from aiogram.types import Message, update

from config import TOKEN, chat_id, admin_id
from core.filters.basic import MyFilter
from core.handlers.basic import get_start, print_message, startbot, update_pool_info, inline_handler
from core.handlers.callback import callback_handler
from core.handlers.join import greeting, greeting2, joined
from core.middlewares.dbmiddleware import DbSession
from core.middlewares.loggingmiddleware import LoggerMiddleware
from logger import logger, event_logger
from aiogram.filters import Command, ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER


def register_commands(dp: Dispatcher):
    database = 'maindb'
    dp.update.middleware.register(LoggerMiddleware(event_logger))
    dp.update.middleware.register(DbSession(database))
    dp.startup.register(startbot)
    dp.callback_query.register(callback_handler)
    dp.message.register(get_start, Command(commands=['start']))
    dp.message.register(update_pool_info, Command(commands=['update']), F.from_user.id == admin_id)
    # dp.message.register(get_links, Command(commands=['link']))
    dp.message.register(print_message)
    dp.chat_join_request.register(greeting, MyFilter(chat_id))
    dp.chat_join_request.register(greeting2)
    dp.inline_query.register(inline_handler)
    dp.chat_member.register(joined, ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))


async def start_bot():
    bot = Bot(token=TOKEN)
    logger.info('Bot started')
    dp = Dispatcher()
    register_commands(dp)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


async def webhook_start(event, context):
    logger.info(event)
    bot = Bot(token=TOKEN)
    logger.info('Bot started')
    dp = Dispatcher()
    register_commands(dp)
    try:
        up = json.loads(event['body'])

        my_update = update.Update(update_id=up['update_id'], message=up['message'])
        await dp.feed_update(bot=bot, update=my_update)
        return {
            'statusCode': 200,
            'body': '!'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }


if __name__ == '__main__':
    asyncio.run(start_bot())