import asyncio
import logging
import os
from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.types import InputMediaPhoto
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "549415850"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

async def send_log(text: str):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await bot.send_message(OWNER_ID, f"[{now}] {text}")

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer("Бот працює ✅")
    await send_log("Отримано команду /start")

async def hourly_task():
    while True:
        try:
            # Тут має бути логіка парсингу і надсилання нових турів
            await send_log("Парсинг нових турів... (тестове повідомлення)")
        except Exception as e:
            await send_log(f"Помилка під час парсингу: {e}")
        await asyncio.sleep(3600)

async def on_startup(dp):
    asyncio.create_task(hourly_task())
    await send_log("Бот запущено 🟢")

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, on_startup=on_startup)
