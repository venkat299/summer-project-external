# ai_interviewer/config.py

"""
Centralized configuration hub for the AI Interviewer application.
This file contains all the settings and constants used across different modules,
making it easy to manage and update the application's behavior without
hardcoding values directly in the source code.
"""

# --- Local LLM Server (Ollama) Configuration ---
# The base URL for the Ollama API endpoint.
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# The name of the fast, smaller language model used for real-time triage of answers.
# This model should provide quick, preliminary feedback (e.g., correct, incorrect).
TRIAGE_MODEL_NAME = "llama3:8b-instruct-q4_K_M"

# The name of the more powerful and detailed language model used for in-depth analysis.
# This model runs as a background task to provide comprehensive scoring and feedback.
ANALYSIS_MODEL_NAME = "mixtral:8x7b-instruct-q5_K_M"


# --- Audio Processing Configuration ---
# The model identifier for the Speech-to-Text (STT) engine.
# This uses the faster-whisper implementation with the specified model size.
STT_MODEL = "distil-large-v3"

# The filename of the voice model for the Text-to-Speech (TTS) engine.
# This model file must be downloaded and placed in the appropriate directory for piper-tts.
TTS_VOICE_MODEL = "extern/voices/en_US-lessac-high.onnx"


# --- General Application Settings ---
# The logging level for the application.
# Can be set to "DEBUG", "INFO", "WARNING", "ERROR", or "CRITICAL".
LOG_LEVEL = "INFO"
# ai_interviewer/config.py

"""
Centralized configuration hub for the AI Interviewer application.
This file contains all the settings and constants used across different modules,
making it easy to manage and update the application's behavior without
hardcoding values directly in the source code.
"""

# --- Local LLM Server (Ollama) Configuration ---
# The base URL for the Ollama API endpoint.
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# The name of the fast, smaller language model used for real-time triage of answers.
# This model should provide quick, preliminary feedback (e.g., correct, incorrect).
TRIAGE_MODEL_NAME = "llama3:8b-instruct-q4_K_M"

# The name of the more powerful and detailed language model used for in-depth analysis.
# This model runs as a background task to provide comprehensive scoring and feedback.
ANALYSIS_MODEL_NAME = "mixtral:8x7b-instruct-q5_K_M"


# --- Audio Processing Configuration ---
# The model identifier for the Speech-to-Text (STT) engine.
# This uses the faster-whisper implementation with the specified model size.
STT_MODEL = "distil-large-v3"

# The filename of the voice model for the Text-to-Speech (TTS) engine.
# This model file must be downloaded and placed in the appropriate directory for piper-tts.
TTS_VOICE_MODEL = "extern/voices/en_US-lessac-high.onnx"


# --- General Application Settings ---
# The logging level for the application.
# Can be set to "DEBUG", "INFO", "WARNING", "ERROR", or "CRITICAL".
LOG_LEVEL = "INFO"
