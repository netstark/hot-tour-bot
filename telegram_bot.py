
import os
from aiogram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)

async def send_tours(tours):
    if not tours:
        return
    message = "\n\n".join(tours)
    await bot.send_message(chat_id=549415850, text=message, parse_mode="Markdown")
