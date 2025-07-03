import os
import asyncio
import logging
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, BotCommand, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter

from parser import check_new_tours
from filters import load_filters, save_filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
GROUP_ID = int(os.getenv("GROUP_ID"))
TOUR_CHAT_ID = int(os.getenv("TOUR_CHAT_ID"))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# --- FSM для фільтрів ---
class FilterForm(StatesGroup):
    city = State()
    budget = State()
    days = State()

# --- Команда /start ---
@dp.message(commands=["start"])
async def start(message: types.Message):
    if message.from_user.id == OWNER_ID:
        await message.answer("Бот працює 🟢")

# --- Команда /check ---
@dp.message(commands=["check"])
async def manual_check(message: types.Message):
    if message.from_user.id == OWNER_ID:
        await run_check()

# --- Команда /filters ---
@dp.message(F.text == "/filters")
async def show_filters(message: Message):
    filters = load_filters()
    text = (
        f"🔧 Поточні фільтри:\n"
        f"✈️ Місто вильоту: {filters['departure_city']}\n"
        f"💰 Бюджет: до {filters['max_price']}$\n"
        f"📅 Днів: від {filters['min_days']} до {filters['max_days']}"
    )

    buttons = [
        [InlineKeyboardButton(text="✈️ Змінити місто", callback_data="change_city")],
        [InlineKeyboardButton(text="💰 Змінити бюджет", callback_data="change_budget")],
        [InlineKeyboardButton(text="📅 Змінити тривалість", callback_data="change_days")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer(text, reply_markup=keyboard)

# --- Callback: зміна міста ---
@dp.callback_query(F.data == "change_city")
async def change_city(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введи нове місто вильоту:")
    await state.set_state(FilterForm.city)
    await callback.answer()

@dp.message(StateFilter(FilterForm.city))
async def save_city(message: Message, state: FSMContext):
    filters = load_filters()
    filters["departure_city"] = message.text.strip()
    save_filters(filters)
    await message.answer(f"✅ Місто вильоту оновлено на: {message.text}")
    await state.clear()

# --- Callback: зміна бюджету ---
@dp.callback_query(F.data == "change_budget")
async def change_budget(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введи новий бюджет (наприклад: 800):")
    await state.set_state(FilterForm.budget)
    await callback.answer()

@dp.message(StateFilter(FilterForm.budget))
async def save_budget(message: Message, state: FSMContext):
    try:
        val = int(message.text.strip())
        filters = load_filters()
        filters["max_price"] = val
        save_filters(filters)
        await message.answer(f"✅ Бюджет оновлено на: {val}$")
    except:
        await message.answer("❌ Введи лише число.")
    await state.clear()

# --- Callback: зміна тривалості ---
@dp.callback_query(F.data == "change_days")
async def change_days(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введи тривалість через тире (наприклад: 5-10):")
    await state.set_state(FilterForm.days)
    await callback.answer()

@dp.message(StateFilter(FilterForm.days))
async def save_days(message: Message, state: FSMContext):
    try:
        parts = message.text.strip().split("-")
        min_d, max_d = int(parts[0]), int(parts[1])
        filters = load_filters()
        filters["min_days"] = min_d
        filters["max_days"] = max_d
        save_filters(filters)
        await message.answer(f"✅ Тривалість оновлено: від {min_d} до {max_d} днів")
    except:
        await message.answer("❌ Приклад правильного вводу: 5-10")
    await state.clear()

# --- Відправка турів ---
async def run_check():
    try:
        new_tours = await check_new_tours()
        if new_tours:
            await bot.send_message(GROUP_ID, f"🟢 Знайдено {len(new_tours)} нових турів")
            for tour in new_tours:
                await bot.send_message(TOUR_CHAT_ID, tour)
        else:
            await bot.send_message(TOUR_CHAT_ID, "🟡 Нових турів не знайдено")
    except Exception as e:
        await bot.send_message(GROUP_ID, f"❌ Помилка парсингу: {e}")
        print(e)

# --- Запасна відповідь ---
@dp.message()
async def fallback(message: types.Message):
    if message.from_user.id == OWNER_ID:
        await message.answer("Введи /check, /start або /filters")

# --- Запуск ---
async def main():
    await bot.set_my_commands([
        BotCommand(command="start", description="Запустити бота"),
        BotCommand(command="check", description="Перевірити вручну"),
        BotCommand(command="filters", description="Змінити фільтри"),
    ])
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
