import asyncio
import logging
import os
from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "549415850"))
GROUP_ID = -1002111587283  # ID твоєї групи (логування)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


async def log_to_group(text: str):
    now = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    await bot.send_message(GROUP_ID, f"{now} {text}")


async def send_result(text: str):
    await bot.send_message(OWNER_ID, text)


@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer("Бот працює ✅")
    await log_to_group("Отримано /start")


async def hourly_task():
    while True:
        try:
            await log_to_group("Парсинг нових турів... (тестове повідомлення)")
            # Тут буде основна логіка парсингу і перевірки нових турів
            # await send_result("🆕 Новий тур: ...")
        except Exception as e:
            await log_to_group(f"Помилка під час парсингу: {e}")
        await asyncio.sleep(3600)  # 1 година


async def on_startup(dp):
    asyncio.create_task(hourly_task())
    await log_to_group("Бот запущено 🟢")


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
