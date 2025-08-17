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
    """
    Synthesizes text into speech audio data.

    - Method: Uses the Piper TTS engine to generate WAV audio.
    - Input: A string of text to be spoken.
    - Output: A bytes object containing the raw WAV audio data.
    """
    if not voice or not text:
        return b''
    try:
        # CORRECTED: The synthesize method can return an iterable of byte chunks.
        # We must join them into a single bytes object before sending.
        audio_chunks = []
        for chunk in voice.synthesize(text):
            audio_chunks.append(chunk)
        
        wav_bytes = b"".join(audio_chunks)
        return wav_bytes
    except Exception as e:
        print(f"Error during speech synthesis: {e}")
        return b'[Speech Synthesis Error]'
