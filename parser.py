import os
import asyncio
import logging
import json

from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter, Command

from filters import load_filters
from sent_store import SentStore

async def parse_poehalisnami(filters):
    return ["🔥 Тур з poehalisnami.ua: Назва готелю"]

async def parse_otpusk(filters):
    return ["🌴 Тур з otpusk.ua: Назва готелю"]

async def parse_farvater(filters):
    return ["🌊 Тур з farvater.travel: Назва готелю"]

async def parse_joinup(filters):
    return ["☀️ Тур з joinup.ua: Назва готелю"]

sent_store = SentStore("sent_tours.json")

async def check_all_sites():
    filters = load_filters()
    all_new_tours = []
    
    for parser in [parse_poehalisnami, parse_otpusk, parse_farvater, parse_joinup]:
        try:
            tours = await parser(filters)
            for tour in tours:
                if not sent_store.is_sent(tour):
                    all_new_tours.append(tour)
                    sent_store.mark_as_sent(tour)
        except Exception as e:
            logging.error(f"❌ Помилка у {parser.__name__}: {e}")

    return all_new_tours
