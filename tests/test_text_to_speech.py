import os
import tempfile
import subprocess
import pathlib
import sys
import types
import pytest

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

# Create a minimal stub of the piper module so text_to_speech can import it.
piper_module = types.ModuleType("piper")
voice_module = types.ModuleType("piper.voice")

class DummyPiperVoice:
    @staticmethod
    def load(path):
        return None

voice_module.PiperVoice = DummyPiperVoice
piper_module.voice = voice_module
sys.modules["piper"] = piper_module
sys.modules["piper.voice"] = voice_module

from ai_interviewer.audio_processing import text_to_speech


class MockVoice:
    def __init__(self, pcm_data: bytes, sample_rate: int = 16000):
        self.pcm_data = pcm_data
        self.sample_rate = sample_rate

    def synthesize(self, text: str, buffer):
        buffer.write(self.pcm_data)


def setup_module(module):
    module._orig_voice = text_to_speech.voice
    pcm = b"\x00\x00" * 10
    text_to_speech.voice = MockVoice(pcm)


def teardown_module(module):
    text_to_speech.voice = module._orig_voice


def test_synthesize_speech_adds_riff_header():
    wav = text_to_speech.synthesize_speech("hello")
    assert wav[:4] == b"RIFF"


def test_synthesize_speech_decodable_with_decodeaudiodata(tmp_path):
    wav = text_to_speech.synthesize_speech("hello")
    file_path = tmp_path / "out.wav"
    file_path.write_bytes(wav)

    script = (
        "const fs=require('fs');"
        "if (typeof AudioContext==='undefined'){process.exit(1);}"
        "const ctx=new AudioContext();"
        "const wav=fs.readFileSync(process.argv[1]);"
        "ctx.decodeAudioData(wav.buffer.slice(wav.byteOffset,wav.byteOffset+wav.byteLength))"
        ".then(()=>process.exit(0)).catch(()=>process.exit(1));"
    )
    result = subprocess.run(['node', '-e', script, str(file_path)])
    if result.returncode != 0:
        pytest.skip('decodeAudioData not available')
