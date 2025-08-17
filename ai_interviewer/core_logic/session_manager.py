# ai_interviewer/core_logic/session_manager.py

"""
Manages the lifecycle of interview sessions.

This module provides a simple, thread-safe, in-memory storage solution for
managing active interview sessions. It is responsible for creating, retrieving,
and cleaning up SessionState objects, ensuring that each WebSocket connection
is associated with a unique and persistent state.
"""

import threading
from typing import Dict, Optional

from ai_interviewer.models.schemas import SessionState
from ai_interviewer.core_logic.question_engine import mock_knowledge_graph # To get the start node

# --- In-Memory Session Storage ---

# A private dictionary to store active sessions, mapping session_id to a SessionState object.
# This is suitable for a single-instance deployment. For a multi-instance or
# production environment, this should be replaced with a distributed cache like Redis.
_sessions: Dict[str, SessionState] = {}

# A threading.Lock to ensure that concurrent access to the _sessions dictionary
# is handled safely, preventing race conditions.
_session_lock = threading.Lock()


def get_or_create_session(session_id: str) -> SessionState:
    """
    Retrieves an existing session or creates a new one if it doesn't exist.

    This is the primary function used by the WebSocket endpoint to manage session state.
    It ensures that every connection has a valid state object.

    Args:
        session_id: The unique identifier for the interview session.

    Returns:
        The existing or newly created SessionState object.
    """
    with _session_lock:
        if session_id not in _sessions:
            print(f"Creating new session for session_id: {session_id}")
            # Create a new session state, starting at the graph's designated start_node
            _sessions[session_id] = SessionState(
                session_id=session_id,
                current_node_id=mock_knowledge_graph.get("start_node", "end_node")
            )
        else:
            print(f"Retrieving existing session for session_id: {session_id}")
        
        return _sessions[session_id]


def get_session(session_id: str) -> Optional[SessionState]:
    """
    Retrieves a session if it exists, without creating one.

    Args:
        session_id: The unique identifier for the interview session.

    Returns:
        The SessionState object if found, otherwise None.
    """
    with _session_lock:
        return _sessions.get(session_id)


def remove_session(session_id: str) -> None:
    """
    Removes a session from the in-memory store after it has concluded.

    This is a cleanup utility to prevent the session store from growing indefinitely.

    Args:
        session_id: The unique identifier for the session to be removed.
    """
    with _session_lock:
        if session_id in _sessions:
            print(f"Removing session {session_id} from memory.")
            del _sessions[session_id]
        else:
            print(f"Attempted to remove non-existent session: {session_id}")

