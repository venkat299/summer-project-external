# ai_interviewer/audio_processing/speech_to_text.py

from faster_whisper import WhisperModel
import numpy as np
from ai_interviewer.config import STT_MODEL

try:
    print(f"Loading STT model: {STT_MODEL}...")
    stt_model = WhisperModel(STT_MODEL, device="cuda", compute_type="float16")
    print("STT model loaded successfully.")
except Exception as e:
    print(f"Error loading STT model: {e}. Falling back to CPU.")
    stt_model = WhisperModel(STT_MODEL, device="cpu", compute_type="int8")


def transcribe_audio(audio_bytes: bytes) -> str:
    # ... (function content remains the same)
    if not audio_bytes:
        return ""
    try:
        audio_np = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
        segments, _ = stt_model.transcribe(audio_np, beam_size=5)
        transcription = " ".join([seg.text.strip() for seg in segments])
        return transcription
    except Exception as e:
        print(f"Error during audio transcription: {e}")
        return "[Transcription Error]"
