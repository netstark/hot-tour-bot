import asyncio
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from filters import load_filters
from parser import check_all_sites
from telegram_bot import send_tours

app = FastAPI()
scheduler = AsyncIOScheduler()

@app.on_event("startup")
async def startup():
    scheduler.add_job(periodic_check, "interval", minutes=60)
    scheduler.start()

@app.get("/check")
async def manual_check():
    tours = await periodic_check()
    return {"status": f"Знайдено {len(tours)} нових турів"}

async def periodic_check():
    filters = load_filters()
    new_tours = await check_all_sites(filters)
    if new_tours:
        await send_tours(new_tours)
    return new_tours