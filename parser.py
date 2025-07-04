import asyncio
from parsers.poehalisnami import parse_poehalisnami
from parsers.otpusk import parse_otpusk
from parsers.farvater import parse_farvater
from parsers.joinup import parse_joinup
from sent_store import SentStore

sent_store = SentStore("sent_tours.json")

async def check_all_sites(filters):
    all_new = []
    for func in [parse_poehalisnami, parse_otpusk, parse_farvater, parse_joinup]:
        try:
            results = await func(filters)
            for tour in results:
                if not sent_store.is_sent(tour["id"]):
                    sent_store.mark_as_sent(tour["id"])
                    all_new.append(tour)
        except Exception as e:
            print(f"❌ {func.__name__} failed: {e}")
    return all_new