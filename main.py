from aiogram import Bot, Dispatcher, Router, types , F 
from aiogram.enums import ParseMode
from aiogram.enums import ContentType
from aiogram.filters import Command, StateFilter
from aiogram.types import Message , CallbackQuery ,FSInputFile
from aiogram.types import ReplyKeyboardMarkup , InlineKeyboardMarkup , InlineKeyboardButton , KeyboardButton , ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
import asyncio
from aiogram.exceptions import TelegramForbiddenError
from aiogram.fsm.state import StatesGroup , State
import os
from dotenv import load_dotenv
from buttons import main_keyboard,bookmaker_keyboard,withdrawal_keyboard,main_kb,num_request, keyboard

load_dotenv(".env")


TOKEN = os.getenv("TOKEN")
group_id = os.getenv("GROUP")

bot = Bot(token=TOKEN)
dp = Dispatcher()

onex_photo = "AgACAgIAAxkBAAMKaDc4sUpQMcyp1MfcsE6e2PviwV8AAovyMRttGcBJchrr5PFiTYwBAAMCAAN5AAM2BA"
xIdPhoto = "AgACAgIAAxkBAAMIaDc4qCRsHHq7UchE6-LhTYXI7foAAoryMRttGcBJC8MuYtPctKoBAAMCAAN5AAM2BA"
ucanchangeid = "AgACAgIAAxkBAAMIaDc4qCRsHHq7UchE6-LhTYXI7foAAoryMRttGcBJC8MuYtPctKoBAAMCAAN5AAM2BA"

@dp.message(Command("photos"))
async def get_photos(message: Message):
    await message.answer_photo(onex_photo)
    await message.answer_photo(xIdPhoto)
    await message.answer_photo(ucanchangeid)








# Состояние для запроса 1xBet ID
class DepositState(StatesGroup):
    in_out = State()
    waiting_for_1xbet_id = State()
    waiting_for_deposit_amount = State()
    waiting_for_payment_proof = State()

class withdraw_opt(StatesGroup):
    withdraw_option = State()
    sumofWith = State() 
    phone_num = State()
    xid = State()
    

@dp.message(F.text == "🏠 Главное меню")
@dp.message(Command("start"))
async def handle_main_menu(message: Message, state: FSMContext):
    await state.clear()  # сбрасываем любое текущее состояние
    user = message.from_user
    name = user.full_name or user.username or "друг"
    text =\
        (f"Привет, {name}!\n"
        "Пополнение/Вывод средств\n"
        "\n"
        "📤 Пополнение 0%\n"
        "📤 Вывод 0%\n"
        "👨‍💻 Работаем 24/7\n"    
        "✉️ Наш Канал: @royallkg\n"
                        "\n"
                        "💵 Ваши транзакции защищены Финансовой службой\nСлужба Поддержки @@friday1337")
    await message.reply(text, reply_markup=main_keyboard)
    await message.answer("Выберите действие:", reply_markup=main_kb)


# Клавиатура с выбором букмекера
bookmaker_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="1xBet", callback_data="bookmaker_1xbet")
        ]
    ],
    resize_keyboard=True
)


@dp.callback_query(lambda call: call.data == "deposit")
async def handle_deposit(call: CallbackQuery, state: FSMContext):
    await call.answer()

    # Удаляем предыдущие inline-кнопки
    await bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=None
    )

    # Отправляем текст и inline-кнопку
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="Выберите букмекер:",
        reply_markup=bookmaker_keyboard
    )
    await state.set_state(DepositState.in_out)

@dp.callback_query(lambda call: call.data == "bookmaker_1xbet", DepositState.in_out)
async def handle_bookmaker_1xbet(call: CallbackQuery, state: FSMContext):
    await call.answer()

    # Удаляем inline-кнопку «1xBet»
    await bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=None
    )

    await state.update_data(in_out="Пополнить")
    
    await bot.send_photo(chat_id=call.message.chat.id,photo=onex_photo, caption="Пожалуйста, введите ваш ID с 1xBet:")
    await state.set_state(DepositState.waiting_for_1xbet_id)




# @dp.message(F.photo)
# async def get_id_of_photo(message: Message):
#     photo_id = message.photo[-1].file_id
#     await message.answer(f"{photo_id}")


@dp.message(DepositState.waiting_for_1xbet_id)
async def process_1xbet_id(message: Message, state: FSMContext):
    one_x = message.text
    await state.update_data(onexid=message.text)
    if not one_x.isdigit():
        await message.answer("❌ ID должен содержать только цифры. Попробуйте снова:")
        return

    # Сохраняем ID во временное хранилище (если нужно)
    await state.update_data(user_id=one_x)

    # Запрос суммы пополнения
    await message.answer("Введите сумму пополнения KGS (СОМ):\n"
                         "Минимум : 200\n"
                         "Максимум : 100000")
    await state.set_state(DepositState.waiting_for_deposit_amount)

@dp.message(DepositState.waiting_for_deposit_amount)
async def process_deposit_amount(message: types.Message, state: FSMContext):
    amount_text = message.text.strip()

    if not amount_text.isdigit():
        await message.answer("❌ Сумма должна быть числом. Попробуйте снова:")
        return

    amount = int(amount_text)

    if amount < 200 or amount > 100000:
        await message.answer("⚠️ Сумма пополнения должна быть от 200 до 100000 KGS (СОМ). Попробуйте снова:")
        return

    await state.update_data(amount=amount)  

    data = await state.get_data()
    user_id = data.get("user_id")

    await message.answer(
        f"✅ Ваш ID: {user_id}\n"
        f"💵 Сумма пополнения: {amount} СОМ\n\n"
        f"📨 Переведите указанную сумму на следующие реквизиты по номеру телефона:\n"
        f"<b>MBank: <code>0709679545</code>(Нурсултан К.)</b>\n\n"
        f"<b>Optima: <code>0709679545</code>(Нурсултан К.)</b>\n\n"
        f"<b>Bakai: <code>0709679545</code>(Нурсултан К.)</b>\n\n"
        f"<b>О!Деньги: <code>0709679545</code>(Нурсултан К.)</b>\n\n"
        f"📷 После оплаты, пожалуйста, отправьте чек (фото/скрин):",
        parse_mode="HTML"
    )

    await state.set_state(DepositState.waiting_for_payment_proof)


@dp.message(DepositState.waiting_for_payment_proof, F.photo)
async def payment_proof(message : Message, state: FSMContext):
    user_name = message.from_user.first_name
    if user_name is None:
        user_name = message.from_user.username
    photo_id = message.photo[-1].file_id
    data = await state.get_data()
    await bot.send_photo(chat_id=group_id, photo=photo_id, caption=f"АЙДИ - {data["user_id"]}\n{data["in_out"]}")
    await message.answer(f"""✅Ваша заявка принята на проверку!
🆔ID 1XBET: {data["onexid"]}
💵Сумма: {data["amount"]}
Имя: {user_name}

💰Комиссия: 0%

Пожалуйста подождите!

Служба Поддержки - @KgRoyal_bot

""")
    await state.clear()


@dp.callback_query(lambda call: call.data=="withdraw")
async def withdraw_money(call : CallbackQuery, state: FSMContext):
    await call.message.answer("Выберите удобный вам способ вывода средств: ",reply_markup=withdrawal_keyboard)
    await state.set_state(withdraw_opt.withdraw_option)

@dp.callback_query(F.data.in_(["mbank", "optima", "bakai", "odengi"]), StateFilter(withdraw_opt.withdraw_option))
async def withdraw_options(call : CallbackQuery, state: FSMContext):
    if call.data == "mbank":
        await state.set_state(withdraw_opt.phone_num)
        await state.update_data(withdraw_option = "Мбанк")
    elif call.data == "optima":
        await state.set_state(withdraw_opt.phone_num)
        await state.update_data(withdraw_option = "Оптима")
    elif call.data == "bakai":
        await state.set_state(withdraw_opt.phone_num)
        await state.update_data(withdraw_option = "Бакай")
    elif call.data == "odengi":
        await state.update_data(withdraw_option = "О!Деньги")
        await state.set_state(withdraw_opt.phone_num)
    await call.message.answer("Введите сумму пополнения KGS (СОМ):\n"
                         "Минимум : 200\n"
                         "Максимум : 100000")
    await state.set_state(withdraw_opt.sumofWith)

@dp.message(withdraw_opt.sumofWith)
async def WaitForSum(message: Message, state: FSMContext):
    amount_text = message.text.strip()

    if not amount_text.isdigit():
        await message.answer("❌ Сумма должна быть числом. Попробуйте снова:")
        return

    amount = int(amount_text)

    if amount < 200 or amount > 100000:
        await message.answer("⚠️ Сумма пополнения должна быть от 200 до 100000 KGS (СОМ). Попробуйте снова:")
        return
    await state.set_state(withdraw_opt.phone_num)
    await state.update_data(amount=amount)  
    await message.answer("Введите номер телефона для вывода средств или qr-код",reply_markup=num_request)
    




@dp.message(withdraw_opt.phone_num, F.contact)
async def WaitForNumOrContact(message: Message, state: FSMContext):
    phone = message.text
    if phone is None:
        phone = message.contact.phone_number
    print(phone)
    await state.update_data(number=phone)
    await state.set_state(withdraw_opt.xid)
    await message.answer_photo(ucanchangeid, caption="""⚠️ Изменить ID нельзя после пополнения, проверяйте свой ID перед отправкой еще раз
🆔 Введите ID вашего счета 1xbet""")



@dp.message(withdraw_opt.phone_num, F.text)
async def WaitForNumOrText(message: Message, state: FSMContext):
    phone = message.text
    await state.update_data(number=phone)
    await state.set_state(withdraw_opt.xid)
    await message.answer_photo(ucanchangeid, caption="""⚠️ Изменить ID нельзя после пополнения, проверяйте свой ID перед отправкой еще раз
🆔 Введите ID вашего счета 1xbet""")
    

@dp.message(withdraw_opt.phone_num, F.photo)
async def WaitForNumOrPhoto(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    await state.update_data(number={"photo":file_id})
    await state.set_state(withdraw_opt.xid)
    await message.answer_photo(ucanchangeid, caption="""⚠️ Изменить ID нельзя после пополнения, проверяйте свой ID перед отправкой еще раз
🆔 Введите ID вашего счета 1xbet""")





@dp.message(withdraw_opt.xid)
async def how_to_withdraw(message: Message, state: FSMContext):
    await state.update_data(xid = message.text)
    await message.answer("Вы правильно ввели ? ",reply_markup=keyboard)




@dp.callback_query(lambda call: call.data=="cancel")
async def cancelOperation(call : CallbackQuery,state: FSMContext):
    await call.message.answer("Вы отменили действие")
    await bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=None
    )
    await state.clear()
    return 


@dp.callback_query(lambda call: call.data=="send")
async def forwardOperation(call : CallbackQuery,state: FSMContext):
    user_name = call.from_user.first_name
    if user_name is None:
        user_name = call.from_user.username
    await state.update_data(confirm="yes")
    data = await state.get_data()
    number = data["number"]
    if type(number) is dict:
        number_fin = number["photo"]
    else:
        number = data["number"]
    if type(number) is dict:
        await bot.send_photo(photo=number_fin,chat_id=group_id,caption=f"""✅Ваша заявка принята на проверку!
Банк - {data["withdraw_option"]}
Сумма - {data["amount"]}
🆔ID 1XBET: {data["xid"]}
Имя: {user_name}

Служба Поддержки - @KgRoyal_bot
💰Комиссия: 0%
Пожалуйста подождите!
    """)
        await bot.send_photo(photo=number_fin,chat_id=call.message.chat.id,caption=f"""✅Ваша заявка принята на проверку!
Банк - {data["withdraw_option"]}
Сумма - {data["amount"]}
🆔ID 1XBET: {data["xid"]}
Имя: {user_name}

Служба Поддержки - @KgRoyal_bot
💰Комиссия: 0%
Пожалуйста подождите!
    """)
    else:
        await bot.send_message(chat_id=group_id, text=f"""✅Ваша заявка принята на проверку!
Банк - {data["withdraw_option"]}
Номер - {data['number']}
Сумма - {data["amount"]}
🆔ID 1XBET: {data["xid"]}
Имя: {user_name}

Служба Поддержки - @KgRoyal_bot
💰Комиссия: 0%
Пожалуйста подождите!
    """)
        await bot.send_message(chat_id=call.message.chat.id, text=f"""✅Ваша заявка принята на проверку!
Банк - {data["withdraw_option"]}
Номер - {data['number']}
Сумма - {data["amount"]}
🆔ID 1XBET: {data["xid"]}
Имя: {user_name}

Служба Поддержки - @KgRoyal_bot
💰Комиссия: 0%
Пожалуйста подождите!
    """)
        
        
    await state.clear()


    




@dp.message(lambda message: message.text == "🏠 Главное меню")
async def handle_main_menu(message: Message):
    await handle_main_menu(message)

async def main():
    await dp.start_polling(bot)

# Запуск бота
if __name__ == '__main__':
    print("Бот запущен...")
    asyncio.run(main()) # ранним глав функцию 