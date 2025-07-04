import os
import asyncio
from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)

async def send_tours(tours):
    await bot.send_message(GROUP_ID, f"🟢 Знайдено {len(tours)} нових турів")
    for t in tours:
        msg = (
            f"<b>{t['title']}</b>\n"
            f"📍 {t['location']}\n"
            f"🛏️ {t['nights']} ночей\n"
            f"💵 {t['price']}\n"
            f"<a href='{t['link']}'>🔗 Посилання</a>\n"
        )
        await bot.send_photo(chat_id=GROUP_ID, photo=t['image'], caption=msg)