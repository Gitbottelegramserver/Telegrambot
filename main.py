import asyncio
from aiogram import Bot, Dispatcher
from app.dialogs import router  # убедись, что router есть в dialogs.py
from app.config import TOKEN  # токен из config

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_router(router)  # добавляем маршруты (если есть)

# Асинхронный запуск
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# Точка входа
if __name__ == "__main__":
    asyncio.run(main())

