from aiogram import Bot
from aiogram.enums import ParseMode, parse_mode
from aiogram.types import CallbackQuery

from config import chat_id, main_link, support_bot
from core.handlers.basic import get_start
from core.keyboards.basic import BackKeyboard, MainKeyboard, HelpKeyboard
from core.utils.basic import count_weight, get_link
from core.utils.channel import num_of_valid_refs, is_in_channel
from core.utils.database import DbRequest


async def callback_handler(call: CallbackQuery, bot: Bot, request: DbRequest):
    if call.data == 'rules':
        await call.message.edit_text('Привет! Зарегистрируйся через нашего бота, чтобы начать зарабатывать.'
                                     ' Отправь свою ссылку-приглашение друзьям'
                                     ' – чем больше друзей присоединится, тем больше ты заработаешь.'
                                     ' Обязательно подпишись на наш канал, чтобы не пропустить новые задания.'
                                     ' Выполняй задания, которые, возможно, будут появляться позже.'
                                     ' Больше выполненных заданий – больше твой заработок.'
                                     ' Мы делим заработанные деньги между всеми активными пользователями:'
                                     ' чем больше ты участвуешь, тем больше твой заработок!'
                                     ' Пожалуйста, выполняй задания честно'
                                     ' – мошенничество запрещено и приведет к блокировке.'
                                     ' Если у тебя есть вопросы, свяжись с нашей поддержкой через бота. '
                                     'Присоединяйся и начинай зарабатывать с нами легко и просто!',
                                     reply_markup=BackKeyboard)
    if call.data == 'help':
        await call.message.edit_text(f'Можете написать сообщение [сюда]({support_bot})', reply_markup=BackKeyboard,
                                     parse_mode=ParseMode.MARKDOWN_V2)
    if call.data == 'earn':
        weight = await count_weight(bot, call.message.chat.id, request)
        total_weight, money_pool = request.get_pool_info()
        await call.message.edit_text(f'*Твой вклад*: {weight} из {total_weight}\n'
                                     f'*Предварительный доход в этом месяце*: {weight / total_weight * money_pool if total_weight > 0 else 0}\n'
                                     f'Настоящий доход может стать как больше так и меньше.\n'
                                     f'Вклад считается по формуле:\n`1 + 0,2 \* кол-во пришлашенных друзей`.\n'
                                     f'Позже формула будет меняться.'.replace('.','\.'),
                                     reply_markup=BackKeyboard,
                                     parse_mode=ParseMode.MARKDOWN_V2)
    if call.data == 'refs':
        refs = request.get_refs(call.message.chat.id)
        active = await num_of_valid_refs(bot, refs)
        link = await get_link(bot, call.from_user.id, request)
        await call.message.edit_text(f'Вот твоя ссылка: `{link}`\n'
                                     f"Активных друзей: {active}\n"
                                     f"Покинуло канал: {len(refs) - active} {'😢' if len(refs)-active > 0 else '😌'}",
                                     parse_mode = ParseMode.MARKDOWN_V2,
                                     reply_markup=BackKeyboard)
    if call.data == 'wallet':
        # print(call.message.chat.id)
        await call.message.edit_text(f'На вашем балансе: {request.get_balance(call.message.chat.id)}', reply_markup=BackKeyboard)
    if call.data == 'main':
        info = request.get_by_id(call.from_user.id)
        if len(info) > 0 or await is_in_channel(bot, call.from_user.id, chat_id):
            link = await get_link(bot, call.from_user.id, request)
            text = (f'Привет,\n'
                    f'Вот твоя ссылка: `{link}`')
            await call.message.edit_text(text, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=MainKeyboard)
        else:
            text = (f'Привет,\n'
                    f'Для началa вы должны присоединиться к [каналу]({main_link})')
            await call.message.edit_text(text, parse_mode=ParseMode.MARKDOWN_V2)
    if call.data == 'tech_prob':
        pass
    if call.data == 'collab':
        pass
    if call.data == 'complaint':
        pass

    await call.answer()
