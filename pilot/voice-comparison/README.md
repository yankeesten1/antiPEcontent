# Six free local voice auditions

**Selection update:** the user chose **Heart (`af_heart`)**. New videos default to Heart; Sarah was the voice before this audition. The samples below remain the original comparison recordings.

Same script, speed 1.0 and loudness target. Spoken sample numbers identify the voices. No music is included so the voice comparison is clear. No paid API or new model download is needed. These are stock synthetic voices, not recordings of real witnesses. The current video uses Sarah; no replacement is selected until you choose.

[Listen to all six](all-six-voices.mp3)

| Sample | Voice | Accent / type | Start in combined audio |
| --- | --- | --- | --- |
| 1 | [Sarah](01-sarah.mp3) | American female — current voice | 0:00 |
| 2 | [Heart](02-heart.mp3) | American female | 0:13 |
| 3 | [Bella](03-bella.mp3) | American female | 0:27 |
| 4 | [Michael](04-michael.mp3) | American male | 0:41 |
| 5 | [Emma](05-emma.mp3) | British female | 0:57 |
| 6 | [George](06-george.mp3) | British male | 1:09 |

Try Heart and Bella first for alternatives to Sarah; compare Michael and George if you prefer a male narrator. This is a shortlist, not a claim that every listener will prefer them.

After choosing, reproduce a video with:

```sh
.venv/bin/python -m antipe social --audio-preview --voice af_heart --voice-speed 1.0 --output .local/pilot/chosen-voice-new
```

Change af_heart to the chosen key in voices.json. Voice speed supports 0.8–1.2; audition at 1.0 first. British voices use British-English phonemization. Local compute/storage still consume resources, but this implementation has no per-minute speech API bill.
