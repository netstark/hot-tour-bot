import os
import asyncio
import logging
import json

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from parser import check_new_tours
from filters import load_filters, save_filters

from fastapi import FastAPI
from threading import Thread

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
GROUP_ID = int(os.getenv("GROUP_ID"))
TOUR_CHAT_ID = int(os.getenv("TOUR_CHAT_ID"))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

app = FastAPI()

# == Команда старт
@dp.message(Command("start"))
async def cmd_start(message: Message):
    if message.chat.id != OWNER_ID:
        return
    await message.answer("Бот працює 🟢")

    tours = await check_new_tours()
    if tours:
        await message.answer(f"🟢 Знайдено {len(tours)} нових турів")
        for tour in tours:
            await bot.send_message(GROUP_ID, tour)
    else:
        await message.answer("🟡 Нових турів не знайдено")

# == Зміна міста
@dp.message(lambda m: m.text and m.text.startswith("✈️ Змінити місто"))
async def change_city(message: Message, state: FSMContext):
    if message.chat.id != OWNER_ID:
        return
    await message.answer("Введи нове місто вильоту:")
    await state.set_state("waiting_for_city")

@dp.message(lambda m: True)
async def get_city(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == "waiting_for_city":
        filters = load_filters()
        filters["departure_city"] = message.text
        save_filters(filters)
        await message.answer(f"Місто вильоту змінено на: {message.text}")
        await state.clear()

# == HTTP endpoint перевірки
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

# == Запуск бота в окремому потоці
def start_polling():
    asyncio.run(dp.start_polling(bot))

Thread(target=start_polling).start()
