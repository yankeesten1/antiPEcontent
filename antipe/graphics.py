"""Repeatable, local JPEG typography cards; no image-model bill required."""
import hashlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def render_card(directory, title):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    filename = hashlib.sha256(('card-v1:' + title).encode()).hexdigest() + '.jpg'
    path = directory / filename
    if path.exists():
        return filename
    image = Image.new('RGB', (1080, 1080), '#f5f0e6')
    draw = ImageDraw.Draw(image)
    red, ink = '#b73327', '#202925'
    label = ImageFont.load_default(size=25)
    draw.rectangle((0, 0, 1080, 22), fill=red)
    draw.text((76, 90), 'PE / UNDER SCRUTINY', font=label, fill=red)
    draw.line((76, 152, 1004, 152), fill=ink, width=2)
    size = 84
    while True:
        font = ImageFont.load_default(size=size)
        lines, line = [], ''
        for word in title.split():
            trial = (line + ' ' + word).strip()
            if draw.textbbox((0, 0), trial, font=font)[2] > 920 and line:
                lines.append(line)
                line = word
            else:
                line = trial
        lines.append(line)
        if len(lines) * (size + 18) <= 580 or size <= 30:
            break
        size -= 4
    y = 235
    for line in lines:
        draw.text((76, y), line, font=font, fill=ink)
        y += size + 18
    draw.rectangle((76, 861, 160, 875), fill=red)
    draw.text((76, 923), 'CUSTOMERS. WORKERS. COMPETITION.', font=label, fill=ink)
    draw.text((76, 973), 'Read the evidence and context in the caption.', font=ImageFont.load_default(size=23), fill=ink)
    # Concurrent generation writes identical content; replace atomically.
    import tempfile
    import os
    with tempfile.NamedTemporaryFile(dir=directory, suffix='.jpg', delete=False) as temporary:
        temp_path = temporary.name
    try:
        image.save(temp_path, 'JPEG', quality=92)
        os.replace(temp_path, path)
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
    return filename
