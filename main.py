import os
import asyncio
import logging
import json

from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, BotCommand, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter, Command

from parser import check_new_tours
from filters import load_filters, save_filters

from fastapi import FastAPI
app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
TOUR_CHAT_ID = int(os.getenv("TOUR_CHAT_ID"))

# logging can be removed if not needed
# logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

@dp.message(Command("start"))
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

@dp.message(lambda message: message.text == "✈️ Змінити місто")
async def change_city(message: Message):
    if message.chat.id != OWNER_ID:
        return
    await message.answer("Введи нове місто вильоту:")

    @dp.message()
    async def get_new_city(msg: Message):
        filters = load_filters()
        filters["departure_city"] = msg.text
        save_filters(filters)
        await msg.answer(f"Місто вильоту змінено на: {msg.text}")

@app.get("/check")
async def check():
    try:
        new_tours = await check_new_tours()
        if new_tours:
            for tour in new_tours:
                await bot.send_message(TOUR_CHAT_ID, f"🟢 Знайдено 1 нових турів\n{tour}")
            return {"status": f"Знайдено {len(new_tours)} нових турів"}
        return {"status": "🔘 Нових турів не знайдено"}
    except Exception as e:
        await bot.send_message(TOUR_CHAT_ID, f"❌ Помилка парсингу: {e}")
        return {"status": "Помилка"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
