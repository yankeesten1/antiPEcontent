"""Offline voice-preview and original music bed for motion graphics."""
import array
import math
import subprocess
import wave
from pathlib import Path


def speak_line(text, work, index):
    source = work / f'line-{index}.txt'
    result = work / f'line-{index}.wav'
    source.write_text(text)
    subprocess.run([
        'ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-f', 'lavfi',
        '-i', f'flite=textfile={source}:voice=slt', '-ar', '48000', '-ac', '1',
        '-c:a', 'pcm_s16le', str(result)
    ], check=True, capture_output=True)
    with wave.open(str(result)) as audio:
        seconds = audio.getnframes() / audio.getframerate()
    # Give each line time to finish, with breathing room. Never truncate speech.
    frames = max(96, math.ceil((seconds + .6) * 24))
    return result, frames


def join_narration(lines, frames, destination):
    rate = 48000
    with wave.open(str(destination), 'wb') as out:
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(rate)
        for line, count in zip(lines, frames):
            with wave.open(str(line)) as audio:
                if audio.getframerate() != rate or audio.getnchannels() != 1 or audio.getsampwidth() != 2:
                    raise ValueError('Narration stems must be mono, 48 kHz, signed 16-bit PCM WAV')
                data = audio.readframes(audio.getnframes())
            target = int(count / 24 * rate)
            leading = int(.15 * rate)
            spoken = len(data) // 2
            trailing = target - leading - spoken
            if trailing < 0:
                raise ValueError('Voiceover does not fit its scene; extend the scene instead of cutting speech')
            out.writeframes(b'\0\0' * leading + data + b'\0\0' * trailing)


def original_music(destination, seconds):
    """A quiet, original pulse/pad; no sampled recordings or borrowed melody."""
    rate = 48000
    samples = array.array('h')
    # Two restrained chords, with a low pulse. The voice remains dominant.
    chords = [(130.8128, 155.5635, 195.9977), (103.8262, 130.8128, 155.5635)]
    for sample in range(round(seconds * rate)):
        t = sample / rate
        chord = chords[int(t // 8) % 2]
        edge = min(1.0, t / 1.2, max(0.0, seconds - t) / 1.4)
        pad = sum(math.sin(2 * math.pi * frequency * t) for frequency in chord) / 3
        pulse_phase = t % .75
        pulse = math.exp(-pulse_phase * 14) * math.sin(2 * math.pi * 65.4064 * t)
        value = edge * (.10 * pad + .065 * pulse)
        samples.append(max(-32767, min(32767, round(value * 32767))))
    import sys
    if sys.byteorder != 'little':
        samples.byteswap()
    with wave.open(str(destination), 'wb') as out:
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(rate)
        out.writeframes(samples.tobytes())


def mix_reel(video, narration, music, destination):
    subprocess.run([
        'ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
        '-i', str(video), '-i', str(narration), '-i', str(music),
        '-filter_complex',
        '[1:a]loudnorm=I=-16:TP=-2:LRA=7,asplit=2[voice][key];'
        '[2:a]volume=0.75[bed];'
        '[bed][key]sidechaincompress=threshold=0.04:ratio=5:attack=15:release=250[ducked];'
        '[voice][ducked]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.89[mix]',
        '-map', '0:v:0', '-map', '[mix]', '-c:v', 'copy', '-c:a', 'aac',
        '-b:a', '192k', '-ar', '48000', '-ac', '2', '-shortest',
        '-movflags', '+faststart', str(destination)
    ], check=True, capture_output=True)
