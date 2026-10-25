"""Offline profile assets and a review page for the manual pilot."""
from html import escape
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BIO = 'Private equity, examined. Customers. Workers. Competition. Evidence-led explainers. Opinion labeled. Corrections welcome.'


def add_launch_assets(output, batch):
    output = Path(output)
    profile_path = Path(__file__).resolve().parent.parent / 'pilot' / 'profile.json'
    profile = json.loads(profile_path.read_text())
    (output / 'profile.json').write_text(json.dumps(profile, indent=2) + '\n')
    image = Image.new('RGB', (1080, 1080), '#24332a')
    draw = ImageDraw.Draw(image)
    draw.ellipse((143, 143, 937, 937), outline='#c74938', width=14)
    font = ImageFont.load_default(size=330)
    box = draw.textbbox((0, 0), 'PE', font=font, stroke_width=4)
    x = (1080 - (box[2] - box[0])) / 2 - box[0]
    y = 475 - (box[3] - box[1]) / 2 - box[1]
    draw.text((x, y), 'PE', font=font, fill='#f5f0e6', stroke_width=4)
    draw.rounded_rectangle((355, 665, 725, 691), radius=13, fill='#c74938')
    label = ImageFont.load_default(size=34)
    draw.text((540, 748), 'UNDER SCRUTINY', font=label, fill='#f5f0e6', anchor='mm')
    image.save(output / 'profile-avatar-1080.png')
    image.resize((320, 320), Image.Resampling.LANCZOS).save(output / 'profile-avatar-320.png')
    (output / 'profile-avatar.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080" viewBox="0 0 1080 1080"><rect width="1080" height="1080" fill="#24332a"/><circle cx="540" cy="540" r="397" fill="none" stroke="#c74938" stroke-width="14"/><text x="540" y="590" text-anchor="middle" font-family="Arial,sans-serif" font-weight="bold" font-size="330" fill="#f5f0e6">PE</text><rect x="355" y="665" width="370" height="26" rx="13" fill="#c74938"/><text x="540" y="760" text-anchor="middle" font-family="Arial,sans-serif" font-size="34" fill="#f5f0e6">UNDER SCRUTINY</text></svg>''')
    (output / 'profile-copy.txt').write_text(
        f"WORKING DISPLAY NAME: {profile['display_name']}\n"
        f"HANDLE: @{profile['handle']} (confirmed by you; Instagram access is still pending).\n\n"
        'BIO (121 characters):\n' + BIO + '\n\n'
        'AVATAR: profile-avatar-1080.png (square, designed for a circular crop)\n'
        'POSITION: Critical, evidence-led commentary on private equity, centered on customers, workers and competition.\n'
        'CORRECTIONS: DM a source link with the post and claim you want us to check. Never send passwords, private customer records or confidential work documents.\n'
        'SCHEDULE TARGET: 9 p.m. America/New_York, after account restoration and final editorial approval.\n'
        'PROFILE STATUS: draft copy; nothing has been applied to Instagram. Appeal pending as reported on October 25, 2026; recheck the account before use.\n'
    )
    first = batch['posts'][0]
    (output / 'FIRST-POST-REVIEW.md').write_text(
        '# First post — ready for your review, not approved\n\n'
        f"Graphic: `{first['day']:02d}-{first['id'].lower()}.jpg`\n\n"
        'This introduction states an editorial position. It makes no company-specific allegations and does not depend on the blocked source pages.\n\n'
        + first['caption'] + '\n\n'
        'Before publishing: confirm the display name/handle, preview the actual graphic and caption, choose whether to revise the wording, then explicitly approve the final version. Scheduling and account access are still pending.\n'
    )
    guide = Path(__file__).resolve().parent.parent / 'pilot' / 'TONIGHT.md'
    if guide.exists():
        (output / 'TONIGHT.md').write_bytes(guide.read_bytes())
    (output / 'review.html').write_text(review_html(batch))


def review_html(batch):
    cards = []
    for post in batch['posts']:
        stem = f"{post['day']:02d}-{post['id'].lower()}"
        caption = post['caption']
        if post['sources']:
            caption += '\n\nSource reference (review before publishing):\n' + '\n'.join(source['url'] for source in post['sources'])
        label = 'Source review required' if post['sources'] else 'Editorial draft — review wording'
        cards.append(f'''<article><div class="meta">DAY {post['day']} · DRAFT · {escape(label)}</div><h2>{escape(post['title'])}</h2><img loading="lazy" src="{escape(stem)}.jpg" alt="{escape(post['title'], quote=True)}"><label for="caption-{post['day']}">Editable caption</label><textarea id="caption-{post['day']}" maxlength="2200">{escape(caption)}</textarea><p class="count"></p><p class="hint">{escape(post['hypothesis'])}</p><button type="button" data-editor="caption-{post['day']}" data-filename="{escape(stem)}-caption-edited.txt">Download edited caption</button> <a href="{escape(stem)}.jpg" download>Download image</a></article>''')
    return '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PE / Under scrutiny — offline review</title><style>
*{box-sizing:border-box}body{margin:0;background:#f5f0e6;color:#24332a;font:16px/1.6 system-ui,sans-serif}header,main,footer{max-width:1140px;margin:auto;padding:26px}header{padding-top:44px}h1{font:clamp(34px,5vw,62px)/1.1 Georgia,serif;margin:18px 0}h2{font:30px/1.2 Georgia,serif}.brand{letter-spacing:.09em;font-weight:800;color:#b73327}.notice{border-left:4px solid #b73327;padding:14px 20px;background:#fffaf1}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px}article{background:#fffefa;border:1px solid #d8ddd2;border-radius:9px;padding:24px}img{width:100%;height:auto;display:block;border-radius:4px}.meta,.hint,.count{font-size:13px;color:#687267}label{display:block;font-weight:700;margin:18px 0 6px}textarea{width:100%;min-height:330px;resize:vertical;padding:12px;border:1px solid #d8ddd2;font:15px/1.6 system-ui;color:#24332a}button{background:#24332a;color:white;padding:12px 16px;border:0;border-radius:4px;cursor:pointer;font-weight:650}a{color:#a33025}nav{display:flex;gap:18px;flex-wrap:wrap;margin:20px 0}.avatar{width:92px;border-radius:50%;float:right}.count{text-align:right;margin:2px 0}footer{font-size:13px}@media(max-width:700px){.grid{grid-template-columns:1fr}header,main,footer{padding:20px}.avatar{width:64px}}
</style></head><body><header><img class="avatar" src="profile-avatar-320.png" alt="Working PE Under Scrutiny avatar"><div class="brand">PE / UNDER SCRUTINY</div><h1>Your launch desk.<br>No subscriptions needed.</h1><p>Seven drafts. Local graphics. Your final say.</p><div class="notice"><strong>Offline review only.</strong> Nothing here connects to Instagram or schedules a post. Factual drafts need source verification. Edits are not saved automatically: download each edited caption before closing this page. Your downloads do not update GitHub or the original files.</div><nav><a href="TONIGHT.md">Tonight's checklist</a><a href="profile-copy.txt">Profile copy</a><a href="profile-avatar-1080.png" download>Profile image</a><a href="FIRST-POST-REVIEW.md">First post</a><a href="metrics.csv" download>Metrics sheet</a><a href="REVIEW-BEFORE-PUBLISHING.md">Source checklist</a></nav><p id="status" role="status" aria-live="polite"></p></header><main class="grid">''' + ''.join(cards) + '''</main><footer>Posting target: 9 p.m. America/New_York after account restoration and your approval. This file makes no network requests. No account password or API key is needed.</footer><script>
'use strict';
document.querySelectorAll('textarea').forEach(editor=>{const counter=editor.nextElementSibling;const update=()=>{counter.textContent=editor.value.length+' / 2,200';};editor.addEventListener('input',update);update();});
document.querySelectorAll('button[data-editor]').forEach(button=>button.addEventListener('click',()=>{const editor=document.getElementById(button.dataset.editor);const blob=new Blob([editor.value+'\\n'],{type:'text/plain;charset=utf-8'});const link=document.createElement('a');link.href=URL.createObjectURL(blob);link.download=button.dataset.filename;link.click();setTimeout(()=>URL.revokeObjectURL(link.href),1000);document.getElementById('status').textContent='Caption download requested. Keep your downloaded copy; the original file and GitHub have not changed.';}));
</script></body></html>'''
