# ai_interviewer/audio_processing/speech_to_text.py

"""Utilities for converting speech to text.

The frontend streams audio to the backend as WebM/Opus.  Whisper expects
16‑kHz mono PCM bytes, so this module is responsible for converting the
compressed stream into the appropriate raw format before transcription.
"""

from faster_whisper import WhisperModel
import numpy as np
from ai_interviewer.config import STT_MODEL
from pydub import AudioSegment
import io

try:
    print(f"Loading STT model: {STT_MODEL}...")
    stt_model = WhisperModel(STT_MODEL, device="cuda", compute_type="float16")
    print("STT model loaded successfully.")
except Exception as e:
    print(f"Error loading STT model: {e}. Falling back to CPU.")
    stt_model = WhisperModel(STT_MODEL, device="cpu", compute_type="int8")


def _webm_to_pcm16(audio_bytes: bytes) -> bytes:
    """Decode WebM/Opus bytes into 16‑bit PCM at 16 kHz.

    Pydub uses ffmpeg under the hood.  The resulting audio is mono with a
    sample width of 2 bytes, which matches Whisper's expected input format.
    """

    audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format="webm")
    audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
    return audio.raw_data


def transcribe_audio(audio_bytes: bytes) -> str:
    """Transcribe WebM/Opus audio to text using Whisper."""

    if not audio_bytes:
        return ""

    try:
        pcm_bytes = _webm_to_pcm16(audio_bytes)
        audio_np = np.frombuffer(pcm_bytes, dtype=np.int16).astype(np.float32) / 32768.0
        segments, _ = stt_model.transcribe(audio_np, beam_size=5)
        transcription = " ".join([seg.text.strip() for seg in segments])
        return transcription
    except Exception as e:
        print(f"Error during audio transcription: {e}")
        return "[Transcription Error]"
