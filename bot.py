from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram.utils.markdown import hbold
from aiogram import Router
import asyncio
import config
import logging

bot = Bot(token=config.API_TOKEN)
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

# Обработка нажатий на кнопки
@dp.message(F.text == "📚 Курсы")
async def handle_courses(message: Message):
    await message.answer("""Вот список доступных модулей:
1. Введение
2. DeFi
3. NFT
4. Торговля
5. Аналитика""")




@dp.message(F.text == "🛠 Поддержка")
async def handle_support(message: Message):
    await message.answer("По всем вопросам обращайтесь: @support_username")

@dp.message(F.text == "👤 Профиль")
async def handle_profile(message: Message):
    await message.answer(f"Ваш ID: {message.from_user.id}\nВаше имя: {hbold(message.from_user.full_name)}")

# Обработка кнопки оплаты
@dp.message(F.text == "💰 Оплата")
async def handle_payment(message: Message):
    prices = [LabeledPrice(label="Подписка на ALGO HUB", amount=50000)]  # 500.00 RUB
    await bot.send_invoice(
        chat_id=message.chat.id,
        title="Подписка на ALGO HUB",
        description="Доступ ко всем закрытым материалам",
        payload="subscription_payload",
        provider_token=config.PAYMENT_PROVIDER_TOKEN,
        currency="RUB",
        prices=prices,
        start_parameter="test-invoice"
    )

@dp.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_q: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

@dp.message(F.content_type == types.ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: Message):
    await message.answer("✅ Оплата прошла успешно! Добро пожаловать в закрытый раздел.")

# Запуск бота
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
