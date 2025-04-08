from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests

# Конфигурация платёжных сервисов (замени на реальные значения)
API_URL = "https://example.com/api"
API_KEY = "your_api_key"
COURSE_LINK = "https://yourcourse.com/access"  # Ссылка на курс
TELEGRAM_TOKEN = "your_telegram_bot_token"  # Токен вашего Telegram бота
USDT_WALLET_ADDRESS = "your_usdt_wallet_address"  # Адрес для оплаты в USDT
BANK_ACCOUNT_DETAILS = "your_bank_account_details"  # Реквизиты для банковского перевода

# Функция для обработки команды /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Для оплаты курса отправьте команду /pay.')

# Функция для создания платежного запроса в USDT
def create_usdt_payment_link(user_id):
    # Здесь будет интеграция с криптовалютной платформой (например, создание адреса для оплаты в USDT)
    return f"Для оплаты в USDT используйте следующий адрес: {USDT_WALLET_ADDRESS}"

# Функция для создания запроса на банковский перевод
def create_bank_payment_link(user_id):
    # Здесь можно настроить отправку реквизитов банковского перевода
    return f"Для оплаты через банковский перевод используйте следующие реквизиты: {BANK_ACCOUNT_DETAILS}"

# Функция для создания платежного запроса
def create_payment_link(user_id, payment_method):
    if payment_method == "usdt":
        return create_usdt_payment_link(user_id)
    elif payment_method == "bank":
        return create_bank_payment_link(user_id)
    else:
        # Если не указан метод оплаты, используем стандартный платежный метод
        response = requests.post(f"{API_URL}/create_payment", json={"user_id": user_id, "amount": 100}, headers={"Authorization": f"Bearer {API_KEY}"})
        if response.status_code == 200:
            return response.json().get("payment_link")
    return None

# Функция для проверки статуса платежа
def check_payment(user_id):
    response = requests.get(f"{API_URL}/check_payment", params={"user_id": user_id}, headers={"Authorization": f"Bearer {API_KEY}"})
    if response.status_code == 200:
        return response.json().get("status") == "success"
    return False

# Функция обработки команды /pay
def pay(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    # Определяем метод оплаты: либо USDT, либо банковский перевод
    payment_method = "usdt"  # Установите сюда нужный метод, можно получать через параметры команды
    payment_link = create_payment_link(user_id, payment_method)
    
    if payment_link:
        update.message.reply_text(f'Для оплаты перейдите по ссылке: {payment_link}')
    else:
        update.message.reply_text('Ошибка при создании платежа, попробуйте позже.')

# Функция проверки платежа и выдачи доступа
def check_transaction(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    if check_payment(user_id):
        update.message.reply_text(f'Оплата прошла успешно! Доступ к курсу открыт. Пройдите по ссылке: {COURSE_LINK}')
    else:
        update.message.reply_text('Ваш платеж не был завершен. Пожалуйста, повторите попытку.')

# Основная функция для запуска бота
def main():
    updater = Updater(TELEGRAM_TOKEN)

    # Получаем диспетчера для обработки команд
    dispatcher = updater.dispatcher

    # Регистрируем обработчики команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("pay", pay))
    dispatcher.add_handler(CommandHandler("check", check_transaction))

    # Запускаем бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
