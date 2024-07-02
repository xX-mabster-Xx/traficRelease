from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

MainKeyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Информация",
            callback_data="rules"
        ),
        InlineKeyboardButton(
            text="Помощь",
            callback_data="help"
        ),
    ],
    [
        InlineKeyboardButton(
            text="Заработок",
            callback_data="earn"
        ),
        InlineKeyboardButton(
            text="Рефералы",
            callback_data="refs"
        ),
    ],
    [
        InlineKeyboardButton(
            text="Кошелек",
            callback_data="wallet"
        ),
    ]
])

BackKeyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='◀️Назад',
            callback_data="main"
        )
    ]
])

HelpKeyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Техническая проблема',
                callback_data="tech_prob"
            )
        ],
        [
            InlineKeyboardButton(
                text='Сотрудничество',
                callback_data="collab"
            )
        ],
        [
            InlineKeyboardButton(
                text='Жалобы и Предложения',
                callback_data="complaint"
            )
        ],
        [
            InlineKeyboardButton(
                text='◀️Назад',
                callback_data="main"
            )
        ]
    ]
)