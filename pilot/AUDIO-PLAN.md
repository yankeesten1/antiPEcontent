# Music and natural narration

Final narration preference: **natural AI narrator**, user-confirmed. No paid narration service is connected or authorized for spending yet. The downloadable audio prototype uses an offline synthetic voice for timing and mix review; it is not the proposed final voice quality.

## Planning estimate — not a verified live quote

Assume a usage-based voice rate of **$0.015 per generated minute** for illustration. This rate has not been checked against the provider's current price page from this restricted environment. It is not a quote or a guarantee of availability.

| Scenario | Generated minutes/month | Illustrative narration cost |
| --- | ---: | ---: |
| One 30-second post daily, 30 days | 15 | $0.23 |
| One 60-second post daily, 30 days | 30 | $0.45 |
| Three takes per 30-second post | 45 | $0.68 |
| Three takes per 60-second post | 90 | $1.35 |

Set aside **$1–$3/month for narration alone** as a preliminary planning range. Provider minimums, subscription plans, taxes, different models and additional retries can change the cost. ChatGPT subscriptions do not provide general API credits. Research, video hosting, ads and labor are separate. Get a current provider-specific price and user approval before creating a paid account, entering billing details or making a billable voice request. No paid voice calls have been made by this program.

Generate the final voice only after the script is approved. Do not pay to narrate every discarded draft. Use a clear documentary delivery; attributed quotations must not sound as if the quoted person actually recorded them. No voice cloning or simulated witness recordings.

## What the preview contains

- A synthetic Flite narration voice, generated locally by FFmpeg. This is an intentionally labeled low-cost timing preview.
- An original, programmatically composed instrumental pulse/pad, with no sampled recordings or borrowed song. It is a production prototype, not a guarantee that the platform will never apply an automated audio flag.
- Music ducking under narration, voice normalization and peak limiting.
- Separate narration/music WAVs, a mixed MP4, actual scene timings and an SRT caption file. Scene lengths expand to preserve complete speech. The old silent storyboard's 4-second timings are approximate; use voiceover-timing.json for the audio export.

No soundtrack subscription or stock-song purchase is needed for this preview. Before posting, listen on phone speakers and headphones and review the final transcript, qualifiers and attributions. The prototype is an introduction, not a verified case report.

Reproduce locally (FFmpeg must include Flite and H.264):

```sh
.venv/bin/python -m antipe social --audio-preview --output .local/pilot/intro-audio-new
```

Keep the existing output folders intact; exports refuse to overwrite prior edits. A premium narrator integration remains pending current-price verification and explicit approval to connect the service. Do not put keys in chat or GitHub.
