from parsers.poehalisnami import get_poehalisnami_tours

async def check_new_tours():
    return get_poehalisnami_tours()