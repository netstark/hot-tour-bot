import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommand
from aiogram.enums import ParseMode
from aiogram.utils.markdown import hbold
from parser import check_new_tours

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
GROUP_ID = int(os.getenv("GROUP_ID"))
TOUR_CHAT_ID = int(os.getenv("TOUR_CHAT_ID"))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

@dp.message(commands=["start"])
async def start(message: types.Message):
    if message.from_user.id == OWNER_ID:
        await message.answer("Бот працює 🟢")

@dp.message(commands=["check"])
async def manual_check(message: types.Message):
    if message.from_user.id == OWNER_ID:
        await run_check()

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

@dp.message()
async def fallback(message: types.Message):
    if message.from_user.id == OWNER_ID:
        await message.answer("Введи /check або /start")

async def main():
    await bot.set_my_commands([
        BotCommand(command="start", description="Запустити бота"),
        BotCommand(command="check", description="Перевірити вручну"),
    ])
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
