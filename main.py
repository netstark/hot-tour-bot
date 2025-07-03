import logging
import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
from parser import check_new_tours
from apscheduler.schedulers.asyncio import AsyncIOScheduler

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))
TOUR_CHAT_ID = int(os.getenv("TOUR_CHAT_ID"))

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
app = FastAPI()
scheduler = AsyncIOScheduler()

@app.post("/")
async def webhook_handler(request: Request):
    data = await request.json()
    update = Update(**data)
    await dp.process_update(update)
    return {"ok": True}

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.answer("Бот працює 🟢")

@app.get("/check")
async def trigger_parse():
    try:
        new_tours = await check_new_tours()
        if new_tours:
            for tour in new_tours:
                await bot.send_message(TOUR_CHAT_ID, tour)
            return {"status": f"Знайдено {len(new_tours)} нових турів"}
        else:
            await bot.send_message(GROUP_ID, "🟡 Нових турів не знайдено")
            return {"status": "Без нових турів"}
    except Exception as e:
        await bot.send_message(GROUP_ID, f"❌ Помилка парсингу: {e}")
        return {"status": "Помилка"}

async def scheduled_parse():
    try:
        new_tours = await check_new_tours()
        if new_tours:
            for tour in new_tours:
                await bot.send_message(TOUR_CHAT_ID, tour)
        else:
            await bot.send_message(GROUP_ID, "🟡 Нових турів не знайдено (авто)")
    except Exception as e:
        await bot.send_message(GROUP_ID, f"❌ Автопомилка: {e}")

@app.on_event("startup")
async def on_startup():
    await bot.set_webhook("https://hot-tour-bot.onrender.com")
    scheduler.add_job(scheduled_parse, trigger="interval", minutes=30)
    scheduler.start()
