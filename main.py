import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    if message.from_user.id != OWNER_ID:
        return
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Привіт", callback_data="hello"))
    await message.answer("Бот запущено!", reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == "hello")
async def hello_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Привіт, господарю!")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
