# ai_interviewer/api/routes.py

"""
Manages the real-time, bidirectional flow of an interview session using WebSockets.
This is the core integration point that orchestrates all other modules.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, BackgroundTasks
from ai_interviewer.audio_processing.speech_to_text import transcribe_audio
from ai_interviewer.audio_processing.text_to_speech import synthesize_speech
from ai_interviewer.core_logic.session_manager import get_or_create_session, remove_session
from ai_interviewer.core_logic.response_analyzer import run_triage_analysis, run_in_depth_analysis
from ai_interviewer.core_logic.question_engine import select_next_question, mock_knowledge_graph
from ai_interviewer.models.schemas import SessionState, TriageResult

router = APIRouter()


@router.websocket("/interview/{session_id}")
async def interview_session(websocket: WebSocket, session_id: str, background_tasks: BackgroundTasks):
    """
    Handles the entire interview flow over a single WebSocket connection.
    """
    await websocket.accept()
    session = get_or_create_session(session_id)
    print(f"Client connected: {session_id}")

    # --- Initial Question ---
    initial_question_node = mock_knowledge_graph["nodes"][session.current_node_id]
    initial_question_text = initial_question_node["question_text"]
    
    initial_audio = synthesize_speech(initial_question_text)
    await websocket.send_bytes(initial_audio)
    print(f"Sent initial question to {session_id}")

    try:
        while True:
            # 1. Receive audio answer from client
            audio_data = await websocket.receive_bytes()
            print(f"Received audio from {session_id}. Length: {len(audio_data)} bytes.")

            # 2. Transcribe
            transcribed_text = transcribe_audio(audio_data)
            if not transcribed_text or transcribed_text == "[Transcription Error]":
                print(f"Transcription failed or empty for {session_id}. Asking to repeat.")
                repeat_audio = synthesize_speech("I'm sorry, I didn't catch that. Could you please repeat your answer?")
                await websocket.send_bytes(repeat_audio)
                continue
            
            print(f"Transcription for {session_id}: {transcribed_text}")
            
            current_question_text = mock_knowledge_graph["nodes"][session.current_node_id]["question_text"]

            # 3. Fast Triage
            triage_result = await run_triage_analysis(transcribed_text, current_question_text)
            print(f"Triage result for {session_id}: {triage_result.signal}")

            # 4. Run in-depth analysis in the background
            background_tasks.add_task(run_in_depth_analysis, session, current_question_text, transcribed_text)

            # 5. Select next question
            next_question_obj = select_next_question(session, triage_result)
            next_question_text = next_question_obj['question_text']
            
            # Update history before sending the next question
            session.interview_history.append({
                "question": current_question_text,
                "answer": transcribed_text,
                "triage": triage_result.model_dump()
            })

            # 6. Synthesize and send next question
            print(f"Next question for {session_id}: {next_question_text}")
            next_audio = synthesize_speech(next_question_text)
            await websocket.send_bytes(next_audio)

            if session.current_node_id == "end_node":
                print(f"Interview ended for {session_id}. Closing connection.")
                break

    except WebSocketDisconnect:
        print(f"Client {session_id} disconnected.")
    except Exception as e:
        print(f"An unexpected error occurred in session {session_id}: {e}")
    finally:
        remove_session(session_id)
        print(f"Session {session_id} cleaned up.")
