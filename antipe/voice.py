"""Optional local neural narration, using pinned upstream model artifacts."""
import hashlib
import os
import tempfile
from pathlib import Path
from urllib.request import Request, urlopen

RELEASE = 'https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/'
# Digests published by GitHub on the upstream release's expanded asset list.
MODELS = {
    'kokoro-v1.0.int8.onnx': 'ae315a79b623f244700e4afb9246c46a26066782e049ba174bf3ba433970ee9c',
    'voices-v1.0.bin': 'bca610b8308e8d99f32e6fe4197e7ec01679264efed0cac9140fe9c29f1fbf7d',
}


def model_directory():
    return Path(os.getenv('ANTIPE_VOICE_DIR', '.local/voice'))


def digest(path):
    with Path(path).open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()


def prepare_voice(directory=None):
    directory = Path(directory) if directory else model_directory()
    directory.mkdir(parents=True, exist_ok=True)
    for name, expected in MODELS.items():
        destination = directory / name
        if destination.exists():
            if digest(destination) != expected:
                raise ValueError(f'Voice model checksum mismatch: {name}. Preserve the file for investigation; it will not be loaded or silently replaced.')
            continue
        with tempfile.NamedTemporaryFile(dir=directory, delete=False) as temporary:
            partial = Path(temporary.name)
            try:
                with urlopen(Request(RELEASE + name, headers={'User-Agent': 'PEUnderScrutiny-voice-setup'}), timeout=60) as response:
                    while block := response.read(1024 * 1024):
                        temporary.write(block)
                temporary.flush()
                if digest(partial) != expected:
                    raise ValueError(f'Downloaded voice model failed its upstream SHA-256 check: {name}')
                partial.replace(destination)
            finally:
                partial.unlink(missing_ok=True)
    return directory


class NeuralVoice:
    def __init__(self, directory=None, voice='af_sarah'):
        directory = Path(directory) if directory else model_directory()
        for name, expected in MODELS.items():
            path = directory / name
            if not path.exists() or digest(path) != expected:
                raise ValueError('Local voice files are missing or invalid. Run python -m antipe prepare-voice; verification must pass before use.')
        try:
            from kokoro_onnx import Kokoro
            import onnxruntime as runtime
        except ImportError:
            raise ValueError('Install the optional local voice dependencies: pip install -r requirements-voice.txt') from None
        options = runtime.SessionOptions()
        runtime.disable_telemetry_events()
        options.intra_op_num_threads = 2
        options.inter_op_num_threads = 1
        session = runtime.InferenceSession(str(directory / 'kokoro-v1.0.int8.onnx'), sess_options=options, providers=['CPUExecutionProvider'])
        self.engine = Kokoro.from_session(session, str(directory / 'voices-v1.0.bin'))
        self.voice = voice

    def write(self, text, destination):
        import soundfile
        audio, rate = self.engine.create(text, voice=self.voice, speed=1.0, lang='en-us')
        soundfile.write(str(destination), audio, rate, subtype='PCM_16')
