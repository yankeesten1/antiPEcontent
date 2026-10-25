# Local neural narration: provenance and cost

The replacement narrator runs Kokoro locally through kokoro-onnx. It does not call a paid speech service or clone a person's voice. No API key is needed. Local CPU time, storage and any hosting you separately choose are still resources; there is no per-minute API bill for this implementation.

- Project / setup: https://github.com/thewh1teagle/kokoro-onnx
- Package version: kokoro-onnx 0.6.1, soundfile 0.13.1.
- Model release: https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.1
- Digest source: https://github.com/thewh1teagle/kokoro-onnx/releases/expanded_assets/model-files-v1.1
- Quantized English model: kokoro-v1.0.int8.onnx, SHA-256 `ae315a79b623f244700e4afb9246c46a26066782e049ba174bf3ba433970ee9c`.
- Voice data: voices-v1.0.bin, SHA-256 `bca610b8308e8d99f32e6fe4197e7ec01679264efed0cac9140fe9c29f1fbf7d`.
- Selected voice: af_heart (Heart), confirmed by the user. The earlier cut used af_sarah.
- Additional stock voices already included in the same model: af_heart, af_bella, am_michael, bf_emma and bm_george. See voice-comparison/README.md for same-script samples. These require no additional model download or paid API. Heart is now the default; voice auditions do not change the selected voice.
- Upstream lists kokoro-onnx under MIT and the model under Apache 2.0. Model binaries are cached locally and not committed or bundled in the launch ZIP.

Downloads use ordinary verified HTTPS and must match the upstream-published digests before loading. Existing model files with a bad checksum are rejected. No trust checks are disabled. The cache is under `.local/voice`, excluded from Git; `ANTIPE_VOICE_DIR` can select another cache directory.

```sh
.venv/bin/python -m pip install -r requirements-voice.txt
.venv/bin/python -m antipe prepare-voice
.venv/bin/python -m antipe social --audio-preview --output .local/pilot/new-audio
```

The replacement video uses **stationary frames and clean cuts**. There is no zoom, pan or scale animation. The music is a newly arranged instrumental with audible melody, percussion and harmony, not the earlier bass pad. The final mix normalizes the music and lightly lowers it under speech. A separate music-only video is included to make soundtrack review straightforward. Audio and motion quality remain subject to your review; a neural narrator is not a human recording.

Voice audition command: `.venv/bin/python -m antipe compare-voices --output .local/pilot/voices-new`. The samples use a common script, speed 1.0, matched loudness target and no music. Each is labeled with a spoken sample number/name. After selection, use `social --audio-preview --voice <key> --voice-speed 1.0 --output <new-folder>`. Speed accepts 0.8–1.2. The account's saved voice is not changed by auditioning.
