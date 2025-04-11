from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()

# Стейт для навигации по модулям
class LearningFlow(StatesGroup):
    choosing_module = State()

# Старт запроса
@router.message(F.text.lower() == "🎓 обучение" or F.text.lower() == "модули")
async def show_modules(message: Message, state: FSMContext):
    await state.set_state(LearningFlow.choosing_module)
    await message.answer(
        "Выберите интересующий модуль:
"
        "1. Вводный модуль и безопасность
"
        "2. Арбитраж
"
        "3. Скальп-трейдинг
"
        "4. Smart Money
"
        "5. Волновой анализ
"
        "6. DeFi
"
        "7. Проп трейдинг

"
        "Напиши номер модуля, чтобы узнать подробности."
    )

# Ответы по модулям
@router.message(LearningFlow.choosing_module)
async def handle_module_info(message: Message, state: FSMContext):
    module_number = message.text.strip()
    descriptions = {
        "1": "📘 Модуль 1: Вводный модуль и безопасность

"
             "— Основы крипторынка и блокчейна, безопасность хранения и обмена активов, горячие и холодные кошельки, MetaMask, TrustWallet, CoinGecko, CoinMarketCap и многое другое.",
        "2": "📘 Модуль 2: Арбитраж

"
             "— Что такое арбитраж, страхи и ошибки, термины, биржи, стратегии и схемы, пошаговая работа с Bybit, конкуренция в стакане и ведение отчётности.",
        "3": "📘 Модуль 3: Скальп-трейдинг

"
             "— Фигура треугольник, свечной анализ, CScalp, торговля на объёмах и кластерах, дневные сетапы, стратегии и паттерны, тильт и психология трейдера.",
        "4": "📘 Модуль 4: Smart Money

"
             "— Как действуют крупные игроки, SMC паттерны, поведение ликвидности, анализ крупных объёмов, 4 обучающих конференции по Smart Money.",
        "5": "📘 Модуль 5: Волновой анализ

"
             "— Полное обучение по волновой теории, импульсы и коррекции, работа с Fibonacci, терминалы для трейдинга, дневные и живые сессии.",
        "6": "📘 Модуль 6: DeFi

"
             "— Флип стратегии, ончейн анализ, торговля токенами, фарминг ликвидности, защита от скамов, Solana и Ethereum, обозреватели блокчейна.",
        "7": "📘 Модуль 7: Проп трейдинг

"
             "— Полный курс funded трейдинга: HFT, LFT, ликвидность, Range, живые бэктесты, теория + практика, как пройти в проп-фирму и зарабатывать."
    }

    answer = descriptions.get(module_number, "Введите номер модуля от 1 до 7 для получения описания.")
    await message.answer(answer)
