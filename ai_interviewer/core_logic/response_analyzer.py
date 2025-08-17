# ai_interviewer/core_logic/response_analyzer.py

import httpx
import json
from ai_interviewer.config import OLLAMA_API_URL, TRIAGE_MODEL_NAME, ANALYSIS_MODEL_NAME
from ai_interviewer.models.schemas import TriageResult, SessionState

async def run_triage_analysis(transcribed_text: str, question: str) -> TriageResult:
    # ... (function content remains the same)
    prompt = f"""
    You are an AI technical interviewer. A candidate was asked the following question:
    '{question}'
    The candidate responded:
    '{transcribed_text}'
    Analyze the response. Is it correct, incorrect, or partially correct?
    Respond ONLY with a JSON object with two keys: 'signal' (string: "correct", "incorrect", or "partial") and 'confidence' (float: 0.0 to 1.0).
    """
    payload = {
        "model": TRIAGE_MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(OLLAMA_API_URL, json=payload, timeout=10.0)
            response.raise_for_status()
            
        response_data = json.loads(response.json().get('response', '{}'))
        
        return TriageResult(
            signal=response_data.get("signal", "error"),
            confidence=response_data.get("confidence", 0.0)
        )
    except (httpx.RequestError, json.JSONDecodeError, KeyError) as e:
        return TriageResult(signal="error", confidence=0.0)


async def run_in_depth_analysis(session: SessionState, question: str, transcribed_text: str):
    # ... (function content remains the same)
    prompt = f"""
    You are an expert AI technical evaluator. Your task is to provide a detailed analysis
    of a candidate's answer during an interview.
    
    Interview Context (History): {session.interview_history}
    Question Asked: '{question}'
    Candidate's Answer: '{transcribed_text}'

    Provide a detailed analysis covering:
    1.  **Correctness**: How accurate was the answer?
    2.  **Completeness**: Did the answer cover all key aspects?
    3.  **Clarity**: Was the explanation clear and concise?
    4.  **Confidence**: How confident did the candidate seem?
    5.  **Score**: A numerical score from 1 to 10 for this specific answer.

    Respond ONLY with a JSON object containing keys: "analysis_text", "score".
    """
    payload = {
        "model": ANALYSIS_MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(OLLAMA_API_URL, json=payload, timeout=60.0)
            response.raise_for_status()
    except (httpx.RequestError, json.JSONDecodeError) as e:
        print(f"In-depth analysis failed for session {session.session_id}: {e}")
