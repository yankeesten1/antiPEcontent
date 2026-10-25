"""Same-script auditions for existing local voices; no new model downloads."""
import json
import subprocess
import tempfile
import zipfile
from html import escape
from pathlib import Path

from .voice import NeuralVoice, DEFAULT_VOICE

SCRIPT = 'Private equity. Who owns the business, and what changed after the deal? We trace jobs, prices, and service quality using named records, exact quotations, and verified dates.'
VOICES = [
    ('af_sarah', 'Sarah', 'American female'),
    ('af_heart', 'Heart', 'American female'),
    ('af_bella', 'Bella', 'American female'),
    ('am_michael', 'Michael', 'American male'),
    ('bf_emma', 'Emma', 'British female'),
    ('bm_george', 'George', 'British male'),
]


def export_voice_comparison(output):
    output = Path(output)
    archive = output.with_suffix('.zip')
    if output.exists() or archive.exists():
        raise ValueError('Choose a new output folder to preserve the existing audition files')
    speaker = NeuralVoice()
    output.mkdir(parents=True)
    rows = []
    with tempfile.TemporaryDirectory(prefix='antipe-voices-') as temporary:
        work = Path(temporary)
        segments = []
        elapsed = 0
        for index, (key, name, description) in enumerate(VOICES, 1):
            speaker.voice = key
            raw = work / f'{index:02d}.wav'
            speaker.write(f'Sample {index}. {name}. {SCRIPT}', raw)
            stem = f'{index:02d}-{name.lower()}'
            normalized = work / f'{index:02d}-normalized.wav'
            subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(raw), '-af', 'loudnorm=I=-16:TP=-2:LRA=7,apad=pad_dur=0.6', '-ar', '48000', '-ac', '1', '-c:a', 'pcm_s16le', str(normalized)], check=True, capture_output=True)
            subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(normalized), '-c:a', 'libmp3lame', '-b:a', '128k', str(output / f'{stem}.mp3')], check=True, capture_output=True)
            duration = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(normalized)]))
            rows.append({'sample': index, 'name': name, 'voice': key, 'description': description, 'start_seconds': round(elapsed, 2), 'duration_seconds': round(duration, 2), 'file': f'{stem}.mp3'})
            elapsed += duration
            segments.append(normalized)
        manifest = work / 'segments.txt'
        manifest.write_text('\n'.join(f"file '{segment.name}'" for segment in segments) + '\n')
        subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '1', '-i', str(manifest), '-c:a', 'libmp3lame', '-b:a', '128k', str(output / 'all-six-voices.mp3')], check=True, capture_output=True)
    (output / 'script.txt').write_text(SCRIPT + '\n')
    (output / 'voices.json').write_text(json.dumps(rows, indent=2) + '\n')
    selected = next(name for key, name, _ in VOICES if key == DEFAULT_VOICE)
    markdown = ['# Six free local voice auditions', '', f'Same script, speed 1.0 and loudness target. Spoken sample numbers identify the voices. No music is included so the voice comparison is clear. No paid API or new model download is needed. These are stock synthetic voices, not recordings of real witnesses. The selected voice is {selected}; auditioning does not change that selection.', '', '[Listen to all six](all-six-voices.mp3)', '', '| Sample | Voice | Accent / type | Start in combined audio |', '| --- | --- | --- | --- |']
    cards = []
    for row in rows:
        seconds = int(row['start_seconds'])
        timestamp = f'{seconds // 60}:{seconds % 60:02d}'
        markdown.append(f"| {row['sample']} | [{row['name']}]({row['file']}) | {row['description']} | {timestamp} |")
        cards.append(f"<article><h2>{row['sample']}. {escape(row['name'])}</h2><p>{escape(row['description'])}</p><audio controls preload='none' src='{escape(row['file'])}'></audio><p><a href='{escape(row['file'])}' download>Download sample</a></p></article>")
    markdown += ['', 'Try Heart and Bella first for alternatives to Sarah; compare Michael and George if you prefer a male narrator. This is a shortlist, not a claim that every listener will prefer them.', '', 'After choosing, reproduce a video with:', '', '```sh', '.venv/bin/python -m antipe social --audio-preview --voice af_heart --voice-speed 1.0 --output .local/pilot/chosen-voice-new', '```', '', 'Change af_heart to the chosen key in voices.json. Voice speed supports 0.8–1.2; audition at 1.0 first. British voices use British-English phonemization. Local compute/storage still consume resources, but this implementation has no per-minute speech API bill.']
    (output / 'README.md').write_text('\n'.join(markdown) + '\n')
    (output / 'listen.html').write_text("<!doctype html><html lang='en'><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>PE Under Scrutiny — voice auditions</title><style>body{max-width:900px;margin:40px auto;padding:0 20px;background:#f5f0e6;color:#24332a;font:17px/1.6 system-ui}h1{font-family:Georgia,serif;font-size:42px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:20px}article{padding:22px;background:white;border:1px solid #d8ddd2;border-radius:8px}audio{width:100%}a{color:#a33025}</style><h1>Choose your narrator.</h1><p>Six stock local neural voices. Same script and speed; no music. Heart is the selected account voice. Auditioning does not change your choice.</p><p>Unzip this folder before opening the page. These players make no external requests.</p><p><audio controls preload='none' src='all-six-voices.mp3'></audio></p><div class='grid'>" + ''.join(cards) + '</div></html>')
    with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED) as bundle:
        for file in sorted(output.iterdir()):
            bundle.write(file, arcname=output.name + '/' + file.name)
    return archive
