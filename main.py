import asyncio
import logging

from fastapi import FastAPI
from telegram_bot import send_tours

# Увімкнення логування
logging.basicConfig(level=logging.INFO)

# Створення FastAPI застосунку
app = FastAPI()

@app.get("/")
async def root():
    return {"status": "Бот працює 🟢"}

@app.get("/check")
async def check():
    await send_tours()
    return {"status": "Перевірка виконана"}
