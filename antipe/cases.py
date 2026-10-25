"""Render a manually reviewed case file with checked source snapshots/quotes."""
import hashlib
import json
import zipfile
from pathlib import Path

from PIL import Image

from .social import draw_slide, make_video
from .voice import DEFAULT_VOICE


def validate_case(path):
    path = Path(path)
    case = json.loads(path.read_text())
    if case.get('source_review') != 'checked_against_primary_records_by_assistant':
        raise ValueError('Case requires a recorded primary-source review before rendering')
    source_root = (path.parent / 'sources').resolve()
    sources = {}
    for source in case['sources']:
        file = (source_root / source['snapshot']).resolve()
        if not file.is_relative_to(source_root) or not file.is_file():
            raise ValueError('Source snapshots must be files within the case sources folder')
        raw = file.read_bytes()
        if hashlib.sha256(raw).hexdigest() != source['snapshot_sha256']:
            raise ValueError('Source snapshot changed; re-review the record before updating its case reference')
        if not source['url'].startswith('https://'):
            raise ValueError('Source references must use HTTPS')
        sources[source['id']] = {**source, 'text': raw.decode()}
    if len(sources) != len(case['sources']):
        raise ValueError('Source IDs must be unique')
    for quote in case['quotes']:
        if not quote['locator'] or not quote['attribution']:
            raise ValueError('A quote needs its locator and attribution')
        text = ' '.join(sources[quote['source_id']]['text'].split())
        if ' '.join(quote['exact_text'].split()) not in text:
            raise ValueError('Quoted wording is not present verbatim in the captured source')
    ids = {claim['id'] for claim in case['claims']}
    if len(ids) != len(case['claims']):
        raise ValueError('Claim IDs must be unique')
    for claim in case['claims']:
        if not claim['source_ids'] or any(source not in sources for source in claim['source_ids']):
            raise ValueError('Every factual claim must reference captured sources')
    if not 3 <= len(case['slides']) <= 8:
        raise ValueError('A case needs three to eight readable scenes')
    for slide in case['slides']:
        if not slide['claim_ids'] or any(claim not in ids for claim in slide['claim_ids']):
            raise ValueError('Each scene needs claim/source references')
        if not slide['narration'].strip():
            raise ValueError('Each scene needs narration')
    if len(caption_for(case)) > 2200:
        raise ValueError('Case caption and source URLs exceed Instagram’s caption limit')
    return case


def caption_for(case):
    return case['caption'] + '\n\nSources:\n' + '\n'.join(source['url'] for source in case['sources'] if source.get('caption_reference', True))


def export_case(case_file, output):
    case = validate_case(case_file)
    output = Path(output)
    archive = output.with_suffix('.zip')
    if output.exists() or archive.exists():
        raise ValueError('Choose a new output folder; earlier case reviews are preserved')
    output.mkdir(parents=True)
    slides = [{**slide, 'layout': 'case', 'total': len(case['slides'])} for slide in case['slides']]
    thumbs = []
    for index, slide in enumerate(slides, 1):
        image = draw_slide(slide, index)
        image.save(output / f'carousel-{index:02d}.jpg', quality=94)
        thumbs.append(image.resize((324, 405), Image.Resampling.LANCZOS))
    rows = (len(thumbs) + 1) // 2
    preview = Image.new('RGB', (684, rows * 423 + 12), '#151a17')
    for index, image in enumerate(thumbs):
        preview.paste(image, (12 + (index % 2) * 336, 12 + (index // 2) * 423))
    preview.save(output / 'carousel-preview.jpg', quality=92)
    narration = [{'text': slide['narration']} for slide in slides]
    make_video(output, slides, narration, DEFAULT_VOICE, 1.0)
    for old, new in [('introduction-audio-preview.mp4', 'case-heart.mp4'), ('introduction-reel.mp4', 'case-silent.mp4'), ('music-only-preview.mp4', 'case-music-only.mp4')]:
        (output / old).rename(output / new)
    (output / 'caption.txt').write_text(caption_for(case) + '\n')
    (output / 'narration-script.txt').write_text('\n\n'.join(slide['narration'] for slide in slides) + '\n')
    (output / 'case.json').write_text(json.dumps(case, indent=2, ensure_ascii=False) + '\n')
    notes = [f"# {case['title']} — review draft", '', '**Not approved, scheduled or published.** Heart is the selected voice; the specific script and assets still require user approval.', '', f"Coverage: {case['coverage']}", '', 'Automated checks confirm source snapshot integrity, literal quotation matching and references. They do not independently establish truth, completeness, legal conclusions or claim support. The assistant read the primary records; the user must review the final reporting and assets.', '', '## Claims and sources', '']
    for claim in case['claims']:
        notes += [f"- **{claim['id']} — {claim['kind']}:** {claim['text']} Sources: {', '.join(claim['source_ids'])}. Locator: {claim['locator']}"]
    notes += ['', '## Source records', '']
    for source in case['sources']:
        notes += [f"- **{source['id']}** {source['title']} ({source['date']}). {source['url']} Raw record SHA-256: `{source['raw_sha256']}`. Text snapshot SHA-256: `{source['snapshot_sha256']}`."]
    notes += ['', '## Material limitations', '', *['- ' + item for item in case['limitations']], '', 'Review the MP4 and/or six carousel files with caption.txt. The source cards and narration must retain the allegation labels, denial, dismissal and dated settlement status.', '', '- case-heart.mp4: the Heart-narrated video.', '- case-music-only.mp4: the same case with the soundtrack alone.', '- case-silent.mp4: silent counterpart.', '- narration-captions.srt: narration subtitles.', '- voiceover-timing.json: actual scene timing.', '- sources/: captured primary-source text snapshots.', '']
    (output / 'REVIEW-NOTES.md').write_text('\n'.join(notes))
    source_root = Path(case_file).parent / 'sources'
    with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED) as bundle:
        for file in sorted(output.iterdir()):
            bundle.write(file, arcname=output.name + '/' + file.name)
        for source in case['sources']:
            bundle.write(source_root / source['snapshot'], arcname=output.name + '/sources/' + source['snapshot'])
    return archive
