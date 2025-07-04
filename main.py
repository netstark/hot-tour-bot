
import asyncio
from parser import check_all_sites
from telegram_bot import send_tours
from filters import load_filters

async def main():
    filters = load_filters()
    new_tours = await check_all_sites(filters)
    await send_tours(new_tours)

if __name__ == "__main__":
    asyncio.run(main())
