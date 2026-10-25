# Local neural narration: provenance and cost

The replacement narrator runs Kokoro locally through kokoro-onnx. It does not call a paid speech service or clone a person's voice. No API key is needed. Local CPU time, storage and any hosting you separately choose are still resources; there is no per-minute API bill for this implementation.

- Project / setup: https://github.com/thewh1teagle/kokoro-onnx
- Package version: kokoro-onnx 0.6.1, soundfile 0.13.1.
- Model release: https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.1
- Digest source: https://github.com/thewh1teagle/kokoro-onnx/releases/expanded_assets/model-files-v1.1
- Quantized English model: kokoro-v1.0.int8.onnx, SHA-256 `ae315a79b623f244700e4afb9246c46a26066782e049ba174bf3ba433970ee9c`.
- Voice data: voices-v1.0.bin, SHA-256 `bca610b8308e8d99f32e6fe4197e7ec01679264efed0cac9140fe9c29f1fbf7d`.
- Voice used in the new preview: af_sarah, standard voice supplied with the model.
- Upstream lists kokoro-onnx under MIT and the model under Apache 2.0. Model binaries are cached locally and not committed or bundled in the launch ZIP.

Downloads use ordinary verified HTTPS and must match the upstream-published digests before loading. Existing model files with a bad checksum are rejected. No trust checks are disabled. The cache is under `.local/voice`, excluded from Git; `ANTIPE_VOICE_DIR` can select another cache directory.

```sh
.venv/bin/python -m pip install -r requirements-voice.txt
.venv/bin/python -m antipe prepare-voice
.venv/bin/python -m antipe social --audio-preview --output .local/pilot/new-audio
```

The replacement video uses **stationary frames and clean cuts**. There is no zoom, pan or scale animation. The music is a newly arranged instrumental with audible melody, percussion and harmony, not the earlier bass pad. The final mix normalizes the music and lightly lowers it under speech. A separate music-only video is included to make soundtrack review straightforward. Audio and motion quality remain subject to your review; a neural narrator is not a human recording.
