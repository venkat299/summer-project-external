# ai_interviewer/audio_processing/text_to_speech.py

from piper.voice import PiperVoice
from ai_interviewer.config import TTS_VOICE_MODEL

try:
    print(f"Loading TTS voice model: {TTS_VOICE_MODEL}...")
    voice = PiperVoice.load(TTS_VOICE_MODEL)
    print("TTS voice model loaded successfully.")
except Exception as e:
    print(f"Failed to load TTS voice model: {e}.")
    voice = None

def synthesize_speech(text: str) -> bytes:
    # ... (function content remains the same)
    if not voice or not text:
        return b''
    try:
        wav_bytes = b''.join(list(voice.synthesize_stream_raw(text)))
        return wav_bytes
    except Exception as e:
        print(f"Error during speech synthesis: {e}")
        return b'[Speech Synthesis Error]'
