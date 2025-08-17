# ai_interviewer/core_logic/question_engine.py

"""
The brain of the interviewer. It selects the next question from the
knowledge graph based on the candidate's performance on the previous question.
"""

from ai_interviewer.models.schemas import SessionState, TriageResult
# from knowledge_graph.graph_loader import load_graph # Assuming a graph loader
# from utils.logger import get_logger

# logger = get_logger(__name__)

# --- Knowledge Graph Loading ---
# The knowledge graph is loaded once and cached for performance.
# knowledge_graph = load_graph("python_backend_junior.json")

# This is a placeholder for the actual knowledge graph logic.
# In a real implementation, this would be loaded from a JSON file.
mock_knowledge_graph = {
    "start_node": "node_1",
    "nodes": {
        "node_1": {
            "question_text": "Hello, let's begin. Please explain the difference between a list and a tuple in Python.",
            "skill": "Python Fundamentals",
            "difficulty": "easy",
            "transitions": {
                "correct": "node_2",
                "partial": "node_1_followup",
                "incorrect": "node_1_clarify"
            }
        },
        "node_1_followup": {
            "question_text": "You mentioned one is mutable and the other is not. Can you give a practical example of when you would choose a tuple over a list?",
            "skill": "Python Fundamentals",
            "difficulty": "easy",
            "transitions": { "default": "node_2" }
        },
        "node_1_clarify": {
            "question_text": "Let's break it down. What does it mean for an object to be 'mutable' in Python?",
            "skill": "Python Fundamentals",
            "difficulty": "easy",
            "transitions": { "default": "node_2" }
        },
        "node_2": {
            "question_text": "Great. Now, can you explain what a decorator is in Python and provide a simple use case?",
            "skill": "Python Intermediate",
            "difficulty": "medium",
            "transitions": { "default": "end_node" }
        },
        "end_node": {
            "question_text": "Thank you, that concludes our interview.",
            "skill": "end",
            "difficulty": "none",
            "transitions": {}
        }
    }
}


def select_next_question(state: SessionState, triage: TriageResult) -> dict:
    """
    Selects the next question based on the current state and the last answer's triage.

    - Method: Navigates the loaded knowledge graph. If the triage signal is 'correct',
              it moves to a harder or related node. If 'incorrect', it asks a
              clarifying or easier follow-up question on the same topic.
    - Input: The current SessionState and the TriageResult from the last answer.
    - Output: A dictionary representing the next question node from the knowledge graph.
    """
    current_node_id = state.current_node_id
    current_node = mock_knowledge_graph["nodes"].get(current_node_id)

    if not current_node:
        # logger.error(f"Current node ID '{current_node_id}' not found in knowledge graph.")
        return mock_knowledge_graph["nodes"]["end_node"]

    # Determine the next node based on the triage signal
    transitions = current_node.get("transitions", {})
    next_node_id = transitions.get(triage.signal) or transitions.get("default")

    if not next_node_id:
        # logger.warning(f"No valid transition found for signal '{triage.signal}' from node '{current_node_id}'. Ending interview.")
        return mock_knowledge_graph["nodes"]["end_node"]

    # Update the session state with the new node ID
    state.current_node_id = next_node_id
    
    # logger.info(f"Transitioning from '{current_node_id}' to '{next_node_id}' based on signal '{triage.signal}'.")
    
    return mock_knowledge_graph["nodes"].get(next_node_id)
