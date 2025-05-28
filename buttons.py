from aiogram.types import ReplyKeyboardMarkup , InlineKeyboardMarkup , InlineKeyboardButton , KeyboardButton , ReplyKeyboardRemove



# Reply-клавиатура только с "🏠 Главное меню"
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🏠 Главное меню")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

# Клавиатура с выбором букмекера
bookmaker_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="1xBet", callback_data="bookmaker_1xbet")
        ]
    ],
    resize_keyboard=True
)

# Клавиатура выбора вывода
withdrawal_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Мбанк", callback_data="mbank"),
            InlineKeyboardButton(text="Оптима", callback_data="optima")
        ],
        [
            InlineKeyboardButton(text="Бакай", callback_data="bakai"),
            InlineKeyboardButton(text="О!деньги", callback_data="odengi")
        ]
    ],
    resize_keyboard=True
)

# Inline-клавиатура под сообщением
main_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="💰 Пополнить", callback_data="deposit"),
            InlineKeyboardButton(text="💸 Вывести", callback_data="withdraw")
        ]
    ],
    resize_keyboard=True
)

num_request = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отправить номер", request_contact=True)
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)


keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Отправить", callback_data="send"),
            InlineKeyboardButton(text="Отмена", callback_data="cancel")
        ]
    ]
)
