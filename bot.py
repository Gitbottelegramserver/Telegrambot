from dialogs import router as dialogs_router
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.markdown import hbold
import asyncio
import config
import logging

bot = Bot(token="7859836994:AAFmTHXIohdMVoeV-ohqwmtGr3_iqZgQWyU")

dp = Dispatcher(storage=MemoryStorage())

# Главное меню
def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="📚 Курсы")
    builder.button(text="💰 Оплата")
    builder.button(text="🛠 Поддержка")
    builder.button(text="👤 Профиль")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

# Команда /start
@dp.message(F.text == "/start")
async def cmd_start(message: Message):
    await message.answer("Добро пожаловать в ALGO HUB!", reply_markup=main_menu())

# Курсы
@dp.message(F.text == "📚 Курсы")
async def handle_courses(message: Message):
    await message.answer("Вот список доступных модулей: 1. Введение, 2. DeFi, 3. NFT, 4. Торговля, 5. Аналитика")


# Поддержка
@dp.message(F.text == "🛠 Поддержка")
async def handle_support(message: Message):
    await message.answer("По всем вопросам обращайтесь: @support_username")

# Профиль
@dp.message(F.text == "👤 Профиль")
async def handle_profile(message: Message):
    await message.answer(f"Ваш ID: {message.from_user.id}\nВаше имя: {hbold(message.from_user.full_name)}")

# Оплата
@dp.message(F.text == "💰 Оплата")
async def handle_payment(message: Message):
    await message.answer(
        f"💸 Доступные способы оплаты:\n\n"
        f"📌 USDT (TRC20): `{config.USDT_WALLET}`\n"
        f"🏦 Банк: {config.BANK_NAME}\n"
        f"💳 Карта: `{config.BANK_CARD}`\n"
        f"👤 Получатель: {config.BANK_HOLDER}\n\n"
        f"После оплаты пришлите скриншот чека в поддержку.",
        parse_mode="Markdown"
    )

# Запуск бота
async def main():
    logging.basicConfig(level=logging.INFO)
    dp.include_router(dialogs_router)  # если используешь dialogs
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

