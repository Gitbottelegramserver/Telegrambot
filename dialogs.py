from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()

# Стейт для навигации по модулям
class LearningFlow(StatesGroup):
    choosing_module = State()

# Стартовый запрос
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
    responses = {
        "1": "📘 Модуль 1: Вводный модуль и безопасность — расскажет про основы крипты, безопасность, холодные/горячие кошельки и полезные инструменты.",
        "2": "📘 Модуль 2: Арбитраж — подробное руководство по арбитражу, защите от скама, выбору бирж и стратегиям.",
        "3": "📘 Модуль 3: Скальп-трейдинг — стратегии торговли, настройка CScalp, анализ объёмов и кластеров.",
        "4": "📘 Модуль 4: Smart Money — понимание логики крупных игроков и работа с объёмами.",
        "5": "📘 Модуль 5: Волновой анализ — глубокое обучение по волнам, рискам, стратегиям и терминалам.",
        "6": "📘 Модуль 6: DeFi — флип стратегии, ончейн анализ, фарминг, защита от скама.",
        "7": "📘 Модуль 7: Проп трейдинг — полное обучение funded трейдингу + живые сессии и бектесты."
    }

    answer = responses.get(module_number, "Пожалуйста, введите номер модуля от 1 до 7.")
    await message.answer(answer)
