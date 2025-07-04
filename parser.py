
import logging
from sent_store import SentStore
from parsers.poehalisnami import parse_poehalisnami
from parsers.otpusk import parse_otpusk
from parsers.farvater import parse_farvater
from parsers.joinup import parse_joinup

sent_store = SentStore("sent_tours.json")

async def check_all_sites(filters):
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
