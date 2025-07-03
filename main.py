import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from parser import check_new_tours
from apscheduler.schedulers.asyncio import AsyncIOScheduler

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
GROUP_ID = int(os.getenv("GROUP_ID"))
TOUR_CHAT_ID = int(os.getenv("TOUR_CHAT_ID"))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
scheduler = AsyncIOScheduler()

logging.basicConfig(level=logging.INFO)

async def parse_and_send():
    try:
        new_tours = await check_new_tours()
        if new_tours:
            for tour in new_tours:
                await bot.send_message(TOUR_CHAT_ID, tour)
            await bot.send_message(GROUP_ID, f"🟢 Знайдено {len(new_tours)} нових турів")
        else:
            await bot.send_message(GROUP_ID, "⚪️ Нових турів не знайдено")
    except Exception as e:
        await bot.send_message(GROUP_ID, f"🔴 Помилка парсингу: {e}")

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.answer("Бот працює 🟢")

if __name__ == '__main__':
    async def main():
        scheduler.add_job(parse_and_send, trigger='interval', minutes=1)
        scheduler.start()
        await dp.start_polling()

    asyncio.run(main())
