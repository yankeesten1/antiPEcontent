"""Generate original typography carousels and motion graphics locally."""
import json
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PALETTE = {'yellow': '#eeff58', 'ink': '#151a17', 'cream': '#f5f0e6', 'coral': '#ff674c', 'mint': '#a7f1ce'}
SOURCE = Path(__file__).resolve().parent.parent / 'pilot' / 'introduction-v2.json'


def font(size, bold=True):
    path = Path('/usr/share/fonts/truetype/dejavu') / ('DejaVuSansCondensed-Bold.ttf' if bold else 'DejaVuSans.ttf')
    return ImageFont.truetype(str(path), size) if path.exists() else ImageFont.load_default(size=size)


def draw_slide(slide, index, height=1350):
    background = PALETTE[slide['background']]
    dark = slide['background'] == 'ink'
    ink = PALETTE['cream'] if dark else PALETTE['ink']
    accent = PALETTE['mint'] if dark else PALETTE['coral']
    image = Image.new('RGB', (1080, height), background)
    draw = ImageDraw.Draw(image)
    offset = (height - 1350) // 2

    def text(x, y, value, size, color=ink, bold=True):
        face = font(size, bold)
        # Fit the line inside the design's right safe margin on every font.
        while draw.textbbox((0, 0), value, font=face)[2] > 1000 - x and size > 18:
            size -= 1
            face = font(size, bold)
        draw.text((x, y + offset), value, font=face, fill=color)

    def box(coords, fill, radius=0, outline=None, width=1):
        x1, y1, x2, y2 = coords
        draw.rounded_rectangle((x1, y1 + offset, x2, y2 + offset), radius=radius, fill=fill, outline=outline, width=width)

    text(64, 58, 'PE / UNDER SCRUTINY', 30)
    text(899, 58, f'{index:02d}/05', 25)
    draw.line((64, 125 + offset, 1016, 125 + offset), fill=ink, width=2)
    layout = slide['layout']
    if layout == 'hook':
        text(64, 180, slide['headline'][0], 125)
        text(64, 325, slide['headline'][1], 125)
        text(64, 455, slide['headline'][2], 194)
        box((64, 685, 640, 705), PALETTE['coral'])
        # Original vector-style storefront: a question about ownership, not a
        # fabricated image of a real business or investor.
        box((750, 690, 1000, 872), ink, radius=6)
        for left in (768, 883):
            box((left, 736, left + 93, 838), PALETTE['cream'], radius=3)
        box((732, 667, 1016, 715), PALETTE['coral'], radius=3)
        text(774, 674, 'LOCAL', 28)
        for row, line in enumerate(slide['body'].splitlines()):
            text(64, 895 + row * 68, line, 53)
        box((64, 1080, 1016, 1158), ink, radius=7)
        text(86, 1097, "LET'S CHECK THE EVIDENCE.", 34, PALETTE['yellow'])
    elif layout == 'stakeholders':
        text(64, 170, slide['headline'][0], 165)
        text(64, 350, slide['headline'][1], 133, accent)
        for row, (label, description) in enumerate(slide['rows']):
            y = 590 + row * 185
            box((64, y, 1016, y + 153), '#26352b', radius=9)
            text(90, y + 16, label, 43, accent)
            text(90, y + 84, description, 34, ink, False)
    elif layout == 'questions':
        for row, line in enumerate(slide['headline']):
            text(64, 175 + row * 143, line, 130)
        for row, (label, question) in enumerate(slide['rows']):
            y = 580 + row * 182
            draw.ellipse((64, y + offset, 140, y + 76 + offset), fill=PALETTE['ink'])
            text(86, y + 10, str(row + 1), 38, PALETTE['yellow'])
            text(176, y - 2, label, 48)
            text(176, y + 68, question, 35, ink, False)
        text(64, 1154, 'QUESTIONS FIRST. EVIDENCE BEFORE CONCLUSIONS.', 27)
    elif layout == 'standard':
        for row, line in enumerate(slide['headline']):
            text(64, 175 + row * 150, line, 135)
        for row, line in enumerate(slide['body']):
            text(64, 790 + row * 85, line, 47)
        box((64, 1095, 1016, 1170), ink, radius=7)
        text(85, 1111, 'SCRUTINY > ASSUMPTIONS', 39, PALETTE['cream'])
    elif layout == 'choice':
        for row, line in enumerate(slide['headline']):
            text(64, 180 + row * 124, line, 109)
        for row, label in enumerate(slide['choices']):
            y = 675 + row * 130
            box((64, y, 1016, y + 100), ink, radius=9)
            text(92, y + 20, label, 44, PALETTE['mint'])
        text(64, 1110, 'COMMENT YOUR PICK.', 42)
    else:
        raise ValueError('Unknown social slide layout')
    text(64, 1250, '@PEUnderScrutiny', 29)
    text(790, 1250, 'SWIPE >' if height == 1350 and index < 5 else 'FOLLOW >', 27)
    return image


def export_social(output, video=False):
    output = Path(output)
    archive = output.with_suffix('.zip')
    if output.exists() or archive.exists():
        raise ValueError('Choose a new output folder; existing review assets are preserved')
    if video and not shutil.which('ffmpeg'):
        raise ValueError('FFmpeg is required for video; omit --video to export the carousel only')
    content = json.loads(SOURCE.read_text())
    if len(content['slides']) != 5 or len(content['caption']) > 2200:
        raise ValueError('The introduction must have five slides and an Instagram-length caption')
    output.mkdir(parents=True)
    previews = []
    for index, slide in enumerate(content['slides'], 1):
        image = draw_slide(slide, index)
        image.save(output / f'carousel-{index:02d}.jpg', quality=94)
        previews.append(image.resize((324, 405), Image.Resampling.LANCZOS))
    sheet = Image.new('RGB', (684, 1287), '#151a17')
    for index, preview in enumerate(previews):
        sheet.paste(preview, (12 + (index % 2) * 336, 12 + (index // 2) * 423))
    notes = ImageDraw.Draw(sheet)
    notes.text((360, 930), 'NEW INTRO\n5-CARD STORY\n+ MOTION REEL', font=font(25), fill=PALETTE['yellow'], spacing=18)
    sheet.save(output / 'carousel-preview.jpg', quality=92)
    (output / 'caption.txt').write_text(content['caption'] + '\n')
    (output / 'storyboard.json').write_text(json.dumps(content, indent=2, ensure_ascii=False) + '\n')
    (output / 'optional-voiceover.txt').write_text('\n\n'.join(f"{line['seconds']} seconds: {line['text']}" for line in content['voiceover_optional']) + '\n')
    if video:
        make_video(output, content['slides'])
    (output / 'READ-ME.md').write_text('''# Introduction redesign — draft, not approved

The carousel and reel are alternative versions of the SAME introduction. Choose one first; do not post both back-to-back as different stories.

- Carousel: upload carousel-01.jpg through carousel-05.jpg in numbered order as one Instagram multi-image post. Each is 1080×1350.
- Reel (if included): introduction-reel.mp4 is a 20-second, 1080×1920 H.264 video at 24 fps. It has motion, fades and on-screen text, but no audio track. Add your own voiceover using optional-voiceover.txt or choose audio you have rights to use in Instagram's editor. The text is understandable on mute.
- Use caption.txt, review the exact images/video and approve the final version before posting. This is an editorial introduction, not evidence about a named company. No statistics, fake customer quotes or company-specific allegations are asserted.
- This replaces the plain first-post concept as a proposed visual direction. The rest of the week's content has not yet been redesigned or source-verified. Nothing has been scheduled or published.
- Once account access returns, inspect Instagram's crop and interface overlays before posting. Motion and brighter graphics do not guarantee reach. Compare several posts before deciding which format works.

First-frame hook: “Your town. Their exit plan?” The five-card story asks who benefits, identifies research questions, states the evidence standard, and invites a topic choice.
''')
    with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED) as bundle:
        for file in sorted(output.iterdir()):
            bundle.write(file, arcname=output.name + '/' + file.name)
    return archive


def make_video(output, slides):
    # Five 4-second segments. Limit encoders to two threads so rendering does not
    # overwhelm a small development machine. Intermediate files are temporary.
    with tempfile.TemporaryDirectory(prefix='antipe-reel-') as temporary:
        work = Path(temporary)
        segments = []
        for index, slide in enumerate(slides, 1):
            image = work / f'scene-{index}.png'
            segment = work / f'segment-{index}.mp4'
            draw_slide(slide, index, height=1920).save(image)
            subprocess.run([
                'ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
                '-i', str(image), '-vf',
                "zoompan=z='min(1.025,zoom+0.00026)':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=96:s=1080x1920:fps=24,fade=t=in:st=0:d=0.16,format=yuv420p",
                '-frames:v', '96', '-an', '-c:v', 'libx264', '-threads', '2',
                '-preset', 'veryfast', '-crf', '22', '-movflags', '+faststart', str(segment)
            ], check=True, capture_output=True)
            segments.append(segment)
        manifest = work / 'segments.txt'
        manifest.write_text('\n'.join(f"file '{segment.name}'" for segment in segments) + '\n')
        subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '1', '-i', str(manifest), '-c', 'copy', '-movflags', '+faststart', str(output / 'introduction-reel.mp4')], check=True, capture_output=True)
