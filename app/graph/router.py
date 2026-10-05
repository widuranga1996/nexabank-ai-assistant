from typing import Literal

from app.graph.state import AgentState


Intent = Literal[
    "knowledge_retrieval",
    "research",
    "analytics",
    "direct_response",
]


def route_from_supervisor(state: AgentState) -> Intent:
    """
    Route the workflow based on the Supervisor's intent classification.
    """

    intent = state.get("intent", "").strip().lower()

    valid_intents = {
        "knowledge_retrieval",
        "research",
        "analytics",
        "direct_response",
    }

    if intent not in valid_intents:
        # Safe fallback.
        return "knowledge_retrieval"

    return intent