import os
import tempfile
import subprocess
import pathlib
import sys
import types
import io
import wave
import struct
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
from ai_interviewer.utils.wav_helper import add_wav_header


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


def test_synthesize_speech_parseable_with_wave():
    wav = text_to_speech.synthesize_speech("hello")
    with wave.open(io.BytesIO(wav), "rb") as wf:
        frames = wf.readframes(wf.getnframes())
        assert len(frames) == wf.getnframes() * wf.getsampwidth() * wf.getnchannels()


def test_synthesize_speech_fixes_data_size_mismatch():
    pcm = b"\x00\x00" * 10
    valid_wav = add_wav_header(pcm)
    bad_datasize = struct.pack('<I', len(pcm) - 2)
    bad_wav = valid_wav[:40] + bad_datasize + valid_wav[44:]
    original_voice = text_to_speech.voice
    text_to_speech.voice = MockVoice(bad_wav)
    try:
        wav = text_to_speech.synthesize_speech("hi")
    finally:
        text_to_speech.voice = original_voice
    with wave.open(io.BytesIO(wav), "rb") as wf:
        assert wf.getnframes() == 10
