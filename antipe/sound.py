"""Offline voice-preview and original music bed for motion graphics."""
import array
import math
import subprocess
import wave
from pathlib import Path


def speak_line(text, work, index, speaker):
    source = work / f'line-{index}-native.wav'
    result = work / f'line-{index}.wav'
    speaker.write(text, source)
    subprocess.run([
        'ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
        '-i', str(source), '-ar', '48000', '-ac', '1',
        '-c:a', 'pcm_s16le', str(result)
    ], check=True, capture_output=True)
    with wave.open(str(result)) as audio:
        seconds = audio.getnframes() / audio.getframerate()
    # Give each line time to finish, with breathing room. Never truncate speech.
    frames = max(96, math.ceil((seconds + .6) * 24))
    return result, frames


def join_narration(lines, frames, destination):
    if len(lines) != len(frames):
        raise ValueError('Every narration line needs a matching scene duration')
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
    """Original instrumental: midrange arpeggio, chords, bass and percussion."""
    rate = 48000
    samples = array.array('h')
    chords = [(130.8128, 155.5635, 195.9977), (103.8262, 130.8128, 155.5635),
              (87.3071, 103.8262, 130.8128), (97.9989, 116.5409, 146.8324)]
    beat = 60 / 84
    noise_state = 17
    for sample in range(round(seconds * rate)):
        t = sample / rate
        chord = chords[int(t // (4 * beat)) % 4]
        edge = min(1.0, t / .12, max(0.0, seconds - t) / .8)
        phase = t % beat
        half_phase = t % (beat / 2)
        step = int(t / (beat / 2))
        frequency = chord[(0, 1, 2, 1, 0, 2, 1, 2)[step % 8]] * 4
        pluck = math.sin(2 * math.pi * frequency * half_phase) * math.exp(-half_phase * 10)
        pad = sum(math.sin(2 * math.pi * frequency * 2 * t) for frequency in chord) / 3
        bass = math.sin(2 * math.pi * chord[0] / 2 * phase) * math.exp(-phase * 5)
        kick = math.sin(2 * math.pi * (48 * phase + 2 * (1 - math.exp(-phase * 35)))) * math.exp(-phase * 22)
        noise_state = (1664525 * noise_state + 1013904223) & 0xffffffff
        noise = noise_state / 2147483648 - 1
        snare = noise * math.exp(-phase * 25) if int(t / beat) % 2 else 0
        hat = noise * math.exp(-half_phase * 100)
        value = edge * (.17 * pluck + .06 * pad + .10 * bass + .20 * kick + .10 * snare + .026 * hat)
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
        '[2:a]loudnorm=I=-23:TP=-3:LRA=7[bed];'
        '[bed][key]sidechaincompress=threshold=0.08:ratio=2:attack=15:release=180[ducked];'
        '[voice][ducked]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.89[mix]',
        '-map', '0:v:0', '-map', '[mix]', '-c:v', 'copy', '-c:a', 'aac',
        '-b:a', '192k', '-ar', '48000', '-ac', '2', '-shortest',
        '-movflags', '+faststart', str(destination)
    ], check=True, capture_output=True)


def music_only_reel(video, music, destination):
    subprocess.run([
        'ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(video), '-i', str(music),
        '-map', '0:v:0', '-map', '1:a:0', '-af', 'loudnorm=I=-18:TP=-2:LRA=7',
        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-ac', '2',
        '-shortest', '-movflags', '+faststart', str(destination)
    ], check=True, capture_output=True)
