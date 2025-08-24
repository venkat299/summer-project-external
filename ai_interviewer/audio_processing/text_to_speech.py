# ai_interviewer/audio_processing/text_to_speech.py

import logging
import io
from piper.voice import PiperVoice
from ai_interviewer.config import TTS_VOICE_MODEL
from ai_interviewer.utils.wav_helper import add_wav_header

# --- Logger Setup ---
logger = logging.getLogger(__name__)

try:
    logger.info(f"Loading TTS voice model: {TTS_VOICE_MODEL}...")
    voice = PiperVoice.load(TTS_VOICE_MODEL)
    logger.info("TTS voice model loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load TTS voice model: {e}.", exc_info=True)
    voice = None

def synthesize_speech(text: str) -> bytes:
    """
    Synthesizes text into speech and returns it as a complete WAV file in bytes.

    - Method: Uses an in-memory buffer (io.BytesIO) to have piper-tts write a
              complete WAV file, then retrieves the bytes from the buffer.
    - Input: A string of text to be spoken.
    - Output: A bytes object containing a complete and playable WAV file.
    """
    if not voice or not text:
        return b''
    try:
        # Use an in-memory buffer to capture the WAV output.
        with io.BytesIO() as wav_buffer:
            # The synthesize method can write a complete WAV file directly
            # to a file-like object, which is the most reliable approach.
            voice.synthesize(text, wav_buffer)
            wav_data = wav_buffer.getvalue()

        if not wav_data.startswith(b"RIFF"):
            sample_rate = getattr(voice, "sample_rate", 16000)
            wav_data = add_wav_header(wav_data, sample_rate)

        # Log the request being sent to the browser
        logger.info(f"Synthesized speech for browser. WAV data size: {len(wav_data)} bytes.")

        return wav_data
    except Exception as e:
        logger.error(f"Error during speech synthesis: {e}", exc_info=True)
        return b'[Speech Synthesis Error]'
