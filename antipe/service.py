from datetime import datetime
from zoneinfo import ZoneInfo

from .generate import demo_drafts, generate
from .graphics import render_card


def local_day(settings, instant=None):
    current = instant or datetime.now(ZoneInfo(settings.timezone))
    return current.astimezone(ZoneInfo(settings.timezone)).date().isoformat()


def due(settings, instant=None):
    current = (instant or datetime.now(ZoneInfo(settings.timezone))).astimezone(ZoneInfo(settings.timezone))
    hour, minute = map(int, settings.daily_time.split(':'))
    return (current.hour, current.minute) >= (hour, minute)


def make_batch(settings, store, demo=False, retry=False):
    day = local_day(settings)
    batch_id = store.claim_batch(day, 'demo' if demo else 'researched', retry=retry)
    if batch_id is None:
        return False
    try:
        drafts = demo_drafts() if demo else generate(settings, day)
        for draft in drafts:
            filename = render_card(settings.media_dir, draft['title'])
            if settings.public_base:
                draft['image_url'] = settings.public_base + '/media/' + filename
        store.finish_batch(batch_id, drafts)
        return True
    except Exception:
        store.fail_batch(batch_id, "Generation failed. Check the configured model, OPENAI_API_KEY, network access and provider billing. Use the CLI --retry option after correcting the cause.")
        raise


def scheduler(settings, store, stop):
    while not stop.is_set():
        if due(settings) and settings.openai_key:
            try:
                make_batch(settings, store)
            except Exception:
                print("Daily generation failed; see batch status in the inbox.", flush=True)
        stop.wait(30)
