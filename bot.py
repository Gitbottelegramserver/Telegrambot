import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# Настройки Telegram API
TELEGRAM_TOKEN = ""

# Словарь с описанием направлений
CRYPTO_MODULES_FREE = {
    "Trading": "Трейдинг криптовалют — это торговля на биржах, основанная на анализе рынка.",
    "Mining": "Майнинг — процесс добычи криптовалют с использованием вычислительных мощностей.",
    "NFT": "NFT — уникальные токены, представляющие цифровые активы.",
    "DeFi": "DeFi — децентрализованные финансы, предоставляющие услуги вне банков.",
    "Staking": "Staking — процесс хранения криптовалюты на определенный срок для получения вознаграждений.",
    "Blockchain": "Blockchain — технология блокчейн, основа большинства криптовалют и децентрализованных приложений.",
}

CRYPTO_MODULES_PAID = {
    "Smart Contracts": "Smart Contracts — смарт-контракты, которые автоматически исполняются при выполнении условий.",
}

# База данных пользователей, хранящая информацию о платном доступе
user_data = {}

# Функция отправки транзакции (симуляция успешной транзакции)
def confirm_transaction(transaction_code):
    return transaction_code == "CONFIRM123"

async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton(text=name, callback_data=name)] for name in CRYPTO_MODULES_FREE.keys()
    ]
    
    if user_data.get(update.message.from_user.id, {}).get("paid", False):
        keyboard.append([InlineKeyboardButton(text=name, callback_data=name)] for name in CRYPTO_MODULES_PAID.keys())
    
    keyboard.append([InlineKeyboardButton(text=f"Модуль {i}", callback_data=f"Module{i}") for i in range(1, 8)])
    
    keyboard.append([
        InlineKeyboardButton("Оплата", callback_data="pay"),
        InlineKeyboardButton("Модули", callback_data="modules")
    ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите направление в крипте:", reply_markup=reply_markup)

async def module_info(update: Update, context):
    query = update.callback_query
    await query.answer()
    selected_module = query.data
    
    if selected_module.startswith("Module"):
        selected_module_number = selected_module.replace("Module", "")
        description = f"Описание модуля {selected_module_number}: это общий обзор и использование модуля {selected_module_number}."
        await query.edit_message_text(text=f"Вы выбрали: Модуль {selected_module_number}\n\n{description}")
        return
    
    if selected_module in CRYPTO_MODULES_FREE:
        description = CRYPTO_MODULES_FREE[selected_module]
    elif selected_module in CRYPTO_MODULES_PAID and user_data.get(update.message.from_user.id, {}).get("paid", False):
        description = CRYPTO_MODULES_PAID[selected_module]
    else:
        await query.edit_message_text(text="Этот модуль доступен только для платных пользователей. Чтобы получить доступ, оплатите через /pay.")
        return
    
    await query.edit_message_text(
        text=f"Вы выбрали: {selected_module}\n\n{description}\n\nПожалуйста, подтвердите вашу транзакцию для доступа."
    )
    context.user_data["selected_module"] = selected_module

async def pay(update: Update, context):
    await update.message.reply_text("Введите код транзакции для подтверждения вашей оплаты:")

async def confirm_payment(update: Update, context):
    user_id = update.message.from_user.id
    transaction_code = update.message.text
    
    if confirm_transaction(transaction_code):
        user_data[user_id] = {"paid": True}
        await update.message.reply_text("Транзакция подтверждена! Теперь вы можете выбрать платные модули.")
    else:
        await update.message.reply_text("Неверный код транзакции. Попробуйте снова.")

async def show_modules(update: Update, context):
    keyboard = [
        [InlineKeyboardButton(text=name, callback_data=name)] for name in CRYPTO_MODULES_FREE.keys()
    ]
    
    if user_data.get(update.message.from_user.id, {}).get("paid", False):
        keyboard.append([InlineKeyboardButton(text=name, callback_data=name)] for name in CRYPTO_MODULES_PAID.keys())
    
    keyboard.append([InlineKeyboardButton(text=f"Модуль {i}", callback_data=f"Module{i}") for i in range(1, 8)])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Доступные модули:", reply_markup=reply_markup)

# Главная асинхронная функция
async def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(module_info))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_payment))
    application.add_handler(CommandHandler("pay", pay))
    application.add_handler(CommandHandler("modules", show_modules))
    
    # Запускаем polling
    await application.run_polling()

if __name__ == "__main__":
    try:
        import nest_asyncio
        nest_asyncio.apply()  # Это позволяет повторно использовать уже существующий event loop.
    except ImportError:
        pass
    
    # Здесь нет необходимости использовать asyncio.run(), так как Telegram Application сам управляет event loop.
    import asyncio
    asyncio.run(main())
