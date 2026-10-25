"""Offline launch-kit export. Never calls a model, scheduler or publishing API."""
import csv
import json
import re
import shutil
import zipfile
from pathlib import Path

from .graphics import render_card

DEFAULT_BATCH = Path(__file__).resolve().parent.parent / 'pilot' / 'week-01.json'


def export_pilot(output, batch_path=DEFAULT_BATCH):
    batch = json.loads(Path(batch_path).read_text())
    posts = batch['posts']
    if len(posts) != 7 or len({post['id'] for post in posts}) != 7:
        raise ValueError('The launch kit must contain seven uniquely identified drafts')
    if {post['day'] for post in posts} != set(range(1, 8)):
        raise ValueError('The launch kit must have one draft for each day 1–7')
    for post in posts:
        if not re.fullmatch(r'[A-Za-z0-9_-]{1,32}', post['id']):
            raise ValueError('Post IDs must use letters, numbers, underscores or hyphens')
        if not post['title'].strip() or len(post['title']) > 120:
            raise ValueError('Headlines must contain 1–120 characters')
        caption = post['caption']
        if post['sources']:
            caption += '\n\nSource reference (review before publishing):\n' + '\n'.join(source['url'] for source in post['sources'])
        if len(caption) > 2200:
            raise ValueError(f"{post['id']} exceeds Instagram's caption limit")
    output = Path(output)
    archive = output.parent / (output.name + '.zip')
    if output.exists() or archive.exists():
        raise ValueError('Output or archive already exists. Choose a new folder to preserve any edits.')
    output.mkdir(parents=True)
    review = [f"# {batch['name']}", '', f"**{batch['note']}**", '', 'Seven days are a suggested sequence, not scheduled dates. Default posting target: 9 p.m. America/New_York. Set the date and time yourself in Meta Business Suite.', '', 'Review the exact JPEG and caption, verify supporting sources, make edits, then upload and schedule manually. No files in this kit grant approval or trigger publication.', '']
    for post in posts:
        stem = f"{post['day']:02d}-{post['id'].lower()}"
        generated = render_card(output / '.render-cache', post['title'])
        shutil.copyfile(output / '.render-cache' / generated, output / f'{stem}.jpg')
        caption = post['caption']
        if post['sources']:
            caption += '\n\nSource reference (review before publishing):\n' + '\n'.join(source['url'] for source in post['sources'])
        (output / f'{stem}-caption.txt').write_text(caption + '\n')
        review += [f"## Day {post['day']} — {post['title']}", '', f"Files: `{stem}.jpg`, `{stem}-caption.txt`", '', f"Format: {post['format']}. Hypothesis: {post['hypothesis']}", '', 'Approval: **not approved**. Sources: ' + ('**not retrieved; verify before publication**.' if post['sources'] else 'editorial / methodological draft; no external factual example asserted.'), '', caption, '', 'Before publication:', '']
        review += ['- [ ] ' + check for check in post['claim_checks']]
        review += ['- [ ] Review graphic, caption and final source links.', '- [ ] Approve the final version and manually schedule it.', '']
    shutil.rmtree(output / '.render-cache')
    (output / 'REVIEW-BEFORE-PUBLISHING.md').write_text('\n'.join(review))
    (output / 'content.json').write_text(json.dumps(batch, indent=2, ensure_ascii=False) + '\n')
    with (output / 'metrics.csv').open('w', newline='') as handle:
        fields = ['post_id', 'day', 'format', 'published_at', 'post_url', 'reach_48h', 'saves_48h', 'shares_48h', 'comments_48h', 'profile_visits_48h', 'attributed_follows_48h', 'source_clicks_if_measurable', 'revenue_usd', 'cash_cost_usd', 'labor_minutes', 'notes']
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for post in posts:
            writer.writerow({'post_id': post['id'], 'day': post['day'], 'format': post['format']})
    with (output / 'weekly-review.csv').open('w', newline='') as handle:
        writer = csv.writer(handle)
        writer.writerow(['week', 'start_date', 'end_date', 'posts_published', 'opening_followers', 'closing_followers', 'revenue_usd', 'cash_cost_usd', 'labor_hours', 'hourly_value_usd', 'best_format', 'next_experiment', 'notes'])
        for week in range(1, 9):
            writer.writerow([week] + [''] * 12)
    launch = DEFAULT_BATCH.parent / 'LAUNCH.md'
    if launch.exists():
        shutil.copyfile(launch, output / 'START-HERE.md')
    # Refuse to replace a prior archive, even when its working folder was moved.
    with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED) as bundle:
        for file in sorted(output.iterdir()):
            bundle.write(file, arcname=output.name + '/' + file.name)
    return archive
