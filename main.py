from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    FSInputFile
)

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

import asyncio


TOKEN = "YOUR_BOT_TOKEN"

ADMIN_ID = 660138663


bot = Bot(token=TOKEN)

storage = MemoryStorage()
dp = Dispatcher(storage=storage)


# Состояния
class Booking(StatesGroup):
    name = State()
    phone = State()
    service = State()


# Inline меню
main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="💈 Записаться",
                callback_data="booking"
            )
        ],

        [
            InlineKeyboardButton(
                text="💵 Прайс",
                callback_data="price"
            )
        ],

        [
            InlineKeyboardButton(
                text="📸 Instagram",
                url="https://instagram.com"
            )
        ]
    ]
)


# Старт
@dp.message(CommandStart())
async def start_handler(message: Message):

    photo = FSInputFile("barber.jpg")

    await message.answer_photo(
        photo=photo,
        caption="💈 BARBER AI\n\nСтильные стрижки и атмосфера 🔥",
        reply_markup=main_menu
    )


# Кнопка записи
@dp.callback_query(F.data == "booking")
async def booking_handler(callback: CallbackQuery, state: FSMContext):

    await callback.message.answer(
        "👤 Как вас зовут?"
    )

    await state.set_state(Booking.name)

    await callback.answer()


# Имя
@dp.message(Booking.name)
async def get_name(message: Message, state: FSMContext):

    await state.update_data(name=message.text)

    await message.answer(
        "📞 Введите номер телефона"
    )

    await state.set_state(Booking.phone)


# Телефон
@dp.message(Booking.phone)
async def get_phone(message: Message, state: FSMContext):

    await state.update_data(phone=message.text)

    await message.answer(
        "✂️ На какую услугу хотите записаться?"
    )

    await state.set_state(Booking.service)


# Услуга
@dp.message(Booking.service)
async def get_service(message: Message, state: FSMContext):

    await state.update_data(service=message.text)

    data = await state.get_data()

    await message.answer(
        "🔥 Вы успешно записаны!"
    )

    await bot.send_message(
        ADMIN_ID,
        f"💈 Новая запись!\n\n"
        f"👤 Имя: {data['name']}\n"
        f"📞 Телефон: {data['phone']}\n"
        f"✂️ Услуга: {data['service']}"
    )

    await state.clear()


# Прайс
@dp.callback_query(F.data == "price")
async def price_handler(callback: CallbackQuery):

    await callback.message.answer(
        "💵 Прайс:\n\n"
        "✂️ Стрижка — 1500 ₽\n"
        "🪒 Бритьё — 1000 ₽\n"
        "🔥 Комплекс — 2200 ₽"
    )

    await callback.answer()


# AI-style ответы
@dp.message()
async def all_messages(message: Message):

    text = message.text.lower()

    if "привет" in text:

        await message.answer(
            "🔥 Привет! Добро пожаловать в BARBER AI"
        )

    elif "цена" in text:

        await message.answer(
            "💵 Стрижка стоит 1500 ₽"
        )

    else:

        await message.answer(
            "🤖 Используйте кнопки ниже 👇"
        )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())