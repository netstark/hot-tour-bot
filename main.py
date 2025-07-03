import os
import asyncio
import logging
import json

from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter, Command

from parser import check_all_sites
from filters import load_filters, save_filters

from fastapi import FastAPI
app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
GROUP_ID = int(os.getenv("GROUP_ID"))
TOUR_CHAT_ID = int(os.getenv("TOUR_CHAT_ID"))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Клавіатура фільтрів
filter_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✈️ Місто вильоту", callback_data="change_city")],
    [InlineKeyboardButton(text="💵 Бюджет", callback_data="change_budget")],
    [InlineKeyboardButton(text="🕓 Тривалість (днів)", callback_data="change_duration")],
    [InlineKeyboardButton(text="🏖️ Країна", callback_data="change_country")],
    [InlineKeyboardButton(text="⭐ Рейтинг готелю", callback_data="change_rating")]
])

@dp.message(Command("start"))
async def cmd_start(message: Message):
    if message.chat.id != OWNER_ID:
        return
    await message.answer("Бот працює 🟢")

    tours = await check_all_sites()
    if tours:
        await message.answer(f"🟢 Знайдено {len(tours)} нових турів")
        for tour in tours:
            await bot.send_message(GROUP_ID, tour)
    else:
        await message.answer("🟡 Нових турів не знайдено")

    await message.answer("🔧 Обери, що хочеш змінити:", reply_markup=filter_keyboard)

@dp.callback_query(F.data.startswith("change_"))
async def handle_filter_change(callback: CallbackQuery, state: FSMContext):
    field = callback.data.replace("change_", "")
    await state.set_state(field)
    await callback.message.answer(f"Введи нове значення для: {field.upper()}")
    await callback.answer()

@dp.message(StateFilter("city", "budget", "duration", "country", "rating"))
async def save_filter_value(message: Message, state: FSMContext):
    state_name = await state.get_state()
    filters = load_filters()

    if state_name == "city":
        filters["departure_city"] = message.text

    elif state_name == "budget":
        try:
            filters["max_price"] = int(message.text)
        except ValueError:
            await message.answer("❌ Введи число для бюджету.")
            return

    elif state_name == "duration":
        try:
            min_max = message.text.strip().split("-")
            if len(min_max) != 2:
                raise ValueError
            filters["min_days"] = int(min_max[0])
            filters["max_days"] = int(min_max[1])
        except ValueError:
            await message.answer("❌ Введи тривалість у форматі: 5-10")
            return

    elif state_name == "country":
        filters["country"] = message.text

    elif state_name == "rating":
        try:
            filters["min_rating"] = float(message.text)
        except ValueError:
            await message.answer("❌ Введи рейтинг у числовому форматі, наприклад: 4.5")
            return

    save_filters(filters)
    await message.answer(f"✅ Збережено фільтр для {state_name.upper()}")
    await state.clear()

@app.get("/check")
async def check():
    try:
        new_tours = await check_all_sites()
        if new_tours:
            for tour in new_tours:
                await bot.send_message(GROUP_ID, f"🟢 Знайдено 1 нових турів\n{tour}")
            return {"status": f"Знайдено {len(new_tours)} нових турів"}
        return {"status": "🔘 Нових турів не знайдено"}
    except Exception as e:
        await bot.send_message(GROUP_ID, f"❌ Помилка парсингу: {e}")
        return {"status": "Помилка"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
