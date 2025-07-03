import os
import asyncio
import logging
import json

from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, BotCommand, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter

from parser import check_new_tours
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


@dp.message_handler(commands=["start"])
async def cmd_start(message: Message):
    if message.chat.id != OWNER_ID:
        return

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✈️ Змінити місто", callback_data="change_city")]
    ])

    await message.answer("Бот працює 🟢", reply_markup=keyboard)

    tours = await check_new_tours()
    if tours:
        await message.answer(f"🟢 Знайдено {len(tours)} нових турів")
        for tour in tours:
            await bot.send_message(TOUR_CHAT_ID, tour)
    else:
        await message.answer("🟡 Нових турів не знайдено")


@dp.callback_query_handler(lambda c: c.data == "change_city")
async def ask_city(callback: types.CallbackQuery):
    if callback.message.chat.id != OWNER_ID:
        return
    await callback.message.answer("Введи нове місто вильоту:")

    @dp.message_handler()
    async def save_city(message: Message):
        filters = load_filters()
        filters["departure_city"] = message.text
        save_filters(filters)
        await message.answer(f"Місто вильоту змінено на: {message.text}")


@app.get("/check")
async def check():
    try:
        new_tours = await check_new_tours()
        if new_tours:
            for tour in new_tours:
                await bot.send_message(TOUR_CHAT_ID, tour)
            await bot.send_message(GROUP_ID, f"🟢 Знайдено {len(new_tours)} нових турів")
            return {"status": f"Знайдено {len(new_tours)} нових турів"}
        await bot.send_message(GROUP_ID, "🟡 Нових турів не знайдено")
        return {"status": "🔘 Нових турів не знайдено"}
    except Exception as e:
        await bot.send_message(GROUP_ID, f"❌ Помилка парсингу: {e}")
        return {"status": "Помилка"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
