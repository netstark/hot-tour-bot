import os
import asyncio
import logging
import json

from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import Message, BotCommand, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart

from fastapi import FastAPI
from parser import check_new_tours
from filters import load_filters, save_filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
GROUP_ID = int(os.getenv("GROUP_ID"))
TOUR_CHAT_ID = int(os.getenv("TOUR_CHAT_ID"))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# /start
@router.message(CommandStart())
async def cmd_start(message: Message):
    if message.chat.id != OWNER_ID:
        return
    await message.answer("Бот працює 🟢")

    tours = await check_new_tours()
    if tours:
        await message.answer(f"🟢 Знайдено {len(tours)} нових турів")
        for tour in tours:
            await bot.send_message(TOUR_CHAT_ID, tour)
    else:
        await message.answer("🟡 Нових турів не знайдено")

# Змінити місто
@router.message(lambda m: m.text == "✈️ Змінити місто")
async def change_city(message: Message, state: FSMContext):
    if message.chat.id != OWNER_ID:
        return
    await message.answer("Введи нове місто вильоту:")
    await state.set_state("waiting_for_city")

@router.message()
async def handle_any_message(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == "waiting_for_city":
        filters = load_filters()
        filters["departure_city"] = message.text
        save_filters(filters)
        await message.answer(f"Місто вильоту змінено на: {message.text}")
        await state.clear()

# FastAPI
app = FastAPI()

@app.on_event("startup")
async def on_startup():
    asyncio.create_task(dp.start_polling(bot))

@app.get("/check")
async def check():
    try:
        new_tours = await check_new_tours()
        if new_tours:
            for tour in new_tours:
                await bot.send_message(GROUP_ID, f"🟢 Знайдено 1 нових турів\n{tour}")
            return {"status": f"Знайдено {len(new_tours)} нових турів"}
        return {"status": "🔘 Нових турів не знайдено"}
    except Exception as e:
        await bot.send_message(GROUP_ID, f"❌ Помилка парсингу: {e}")
        return {"status": "Помилка"}
