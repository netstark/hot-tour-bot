
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_cmd(message: Message):
    await message.answer("Бот працює!")

if __name__ == "__main__":
    from asyncio import run
    async def notify_owner():
        await bot.send_message(chat_id=int(os.getenv("OWNER_ID")), text="Бот запущено!")

    run(notify_owner())
    executor.start_polling(dp)
