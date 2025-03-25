import ujson
import logging


logging.basicConfig(level=logging.INFO)

TOKEN = "Строка токена"
BOT_VERSION = 0.1
# База данных хранит выбранные юзером лиги
BOT_DB_NAME = "users_leagues"
# Тестовые данные поддерживаемых лиг
BOT_LEAGUES = {
    "1": "Бундеслига",
    "2": "Серия А",
    "3": "Ла Лига",
    "4": "Турецкая Суперлига",
    "5": "Чемпионат Нидерландов",
    "6": "Про-лига Бельгии",
    "7": "Английская Премьер-лига",
    "8": "Лига 1",
}
# Флаги для сообщений, emoji-код
BOT_LEAGUE_FLAGS = {
    "1": ":Germany:",
    "2": ":Italy:",
    "3": ":Spain:",
    "4": ":Turkey:",
    "5": ":Netherlands:",
    "6": ":Belgium:",
    "7": ":England:",
    "8": ":France:",
}

# Данные redis-клиента
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
# По умолчанию пароля нет. Он будет на сервере
REDIS_PASSWORD = None
