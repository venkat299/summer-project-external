# ai_interviewer/audio_processing/text_to_speech.py

from piper.voice import PiperVoice
from ai_interviewer.config import TTS_VOICE_MODEL
from ai_interviewer.utils.wav_helper import add_wav_header

try:
    print(f"Loading TTS voice model: {TTS_VOICE_MODEL}...")
    voice = PiperVoice.load(TTS_VOICE_MODEL)
    print("TTS voice model loaded successfully.")
except Exception as e:
    print(f"Failed to load TTS voice model: {e}.")
    voice = None

def synthesize_speech(text: str) -> bytes:
    """
    Synthesizes text into speech audio data and packages it as a WAV file.

    - Method: Uses Piper TTS to generate raw PCM audio, then adds a WAV header.
    - Input: A string of text to be spoken.
    - Output: A bytes object containing a complete and playable WAV file.
    """
    if not voice or not text:
        return b''
    try:
        # 1. Synthesize the raw PCM audio data
        audio_chunks = []
        # CORRECTED: The synthesize method returns AudioChunk objects.
        # We need to access the raw bytes via the `.audio` attribute of each chunk.
        for chunk in voice.synthesize(text):
            audio_chunks.append(chunk.audio)
        
        raw_pcm_data = b"".join(audio_chunks)

        # 2. Add the WAV header to the raw data
        # The 'lessac' model uses a 16000Hz sample rate.
        wav_data = add_wav_header(raw_pcm_data, sample_rate=16000)
        
        return wav_data
    except Exception as e:
        print(f"Error during speech synthesis: {e}")
        return b'[Speech Synthesis Error]'
