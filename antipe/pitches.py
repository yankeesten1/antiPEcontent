"""Export five editable story candidates without rendering or publishing videos."""
import html
import json
from pathlib import Path
from urllib.parse import urlparse

from .generate import demo_drafts, generate
from .store import Store


def export_pitches(settings, day, output, demo=False):
    output = Path(output)
    if output.exists():
        raise ValueError('Choose a new output folder; earlier review packs are preserved')
    store = Store(settings.database)
    batch = store.claim_batch(day, 'pitch_demo' if demo else 'pitches')
    if batch is None:
        raise ValueError('This day already has a pitch batch. Check its status before requesting another paid run.')
    try:
        drafts = demo_drafts() if demo else generate(settings, day)
        store.finish_batch(batch, drafts)
    except Exception:
        store.fail_batch(batch, 'Pitch generation failed. Review configuration before retrying; provider charges may already have occurred.')
        raise
    output.mkdir(parents=True)
    package = {'day': day, 'status': 'sample_only' if demo else 'pending_source_review',
               'workflow': 'Pick one → check primary records → edit → render → approve → manual Business Suite upload',
               'pitches': [dict(number=i, **draft) for i, draft in enumerate(drafts, 1)]}
    (output / 'pitches.json').write_text(json.dumps(package, ensure_ascii=False, indent=2) + '\n')
    cards = []
    esc = html.escape
    markdown = [f'# Five story pitches — {day}', '', package['workflow'], '',
                'These are candidates, not verified or approved posts. No videos were rendered and nothing was published.', '']
    for pitch in package['pitches']:
        links = []
        for source in pitch['sources']:
            if urlparse(source['url']).scheme == 'https':
                links.append(f'<li><a href="{esc(source["url"], quote=True)}" rel="noreferrer">{esc(source["title"])}</a></li>')
        cards.append(f'<article><h2>{pitch["number"]}. {esc(pitch["title"])}</h2>'
                     f'<h3>Proposed caption</h3><p>{esc(pitch["caption"])}</p>'
                     f'<h3>Visual direction</h3><p>{esc(pitch["image_brief"])}</p>'
                     f'<details><summary>Research references</summary><ul>{"".join(links)}</ul></details>'
                     f'<p class="choice">To select: reply “Pitch {pitch["number"]}” with any requested changes.</p></article>')
        markdown += [f'## {pitch["number"]}. {pitch["title"]}', '', pitch['caption'], '',
                     '**Visual direction:** ' + pitch['image_brief'], '']
    page = ('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width">'
            '<title>Pick your next story</title><style>body{max-width:850px;margin:32px auto;padding:0 20px;'
            'background:#151a17;color:#f5f0e6;font:18px/1.5 system-ui}article{border:1px solid #a7f1ce;'
            'padding:24px;margin:24px 0}h1,h2,a,.choice{color:#eeff58}p{white-space:pre-wrap}summary{cursor:pointer}</style>'
            f'<h1>Pick your next story</h1><p>{esc(day)} · Five candidates, one finished reel.</p>'
            '<p>Reply with a pitch number and edits. We check the selected story against primary records before rendering. '
            'You review the final video and caption, then upload in Business Suite. This page does not save edits or publish.</p>'
            + ('<p>SAMPLE ONLY — not researched case candidates.</p>' if demo else '')
            + ''.join(cards) + '</html>')
    (output / 'review.html').write_text(page)
    (output / 'PITCHES.md').write_text('\n'.join(markdown) + '\n')
    return output
