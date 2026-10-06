from langgraph.graph import StateGraph, START, END

from app.graph.state import AgentState
from app.graph.router import (
    route_from_supervisor,
    route_after_security,
)

from app.agents.security import security_node
from app.agents.supervisor import supervisor_node
from app.agents.retrieval import retrieval_node
from app.agents.research import research_node
from app.agents.response import response_node
from app.agents.validator import validation_node


def build_graph():

    graph = StateGraph(AgentState)

    # ==========================================
    # Nodes
    # ==========================================

    graph.add_node(
        "security",
        security_node,
    )

    graph.add_node(
        "supervisor",
        supervisor_node,
    )

    graph.add_node(
        "knowledge_retrieval",
        retrieval_node,
    )

    graph.add_node(
        "research",
        research_node,
    )

    graph.add_node(
        "response",
        response_node,
    )

    graph.add_node(
        "validator",
        validation_node,
    )

    # ==========================================
    # START → Security
    # ==========================================

    graph.add_edge(
        START,
        "security",
    )

    # ==========================================
    # Security → Supervisor / END
    # ==========================================

    graph.add_conditional_edges(
        "security",
        route_after_security,
        {
            "allowed": "supervisor",
            "blocked": END,
        },
    )

    # ==========================================
    # Supervisor → Specialized Agent
    # ==========================================

    graph.add_conditional_edges(
        "supervisor",
        route_from_supervisor,
        {
            "knowledge_retrieval": "knowledge_retrieval",
            "research": "research",

            # Temporary routes
            "analytics": "research",
            "direct_response": "response",
        },
    )

    # ==========================================
    # Retrieval → Response
    # ==========================================

    graph.add_edge(
        "knowledge_retrieval",
        "response",
    )

    # ==========================================
    # Research → Response
    # ==========================================

    graph.add_edge(
        "research",
        "response",
    )

    # ==========================================
    # Response → Validator
    # ==========================================

    graph.add_edge(
        "response",
        "validator",
    )

    # ==========================================
    # Validator → END
    # ==========================================

    graph.add_edge(
        "validator",
        END,
    )

    return graph.compile()


graph = build_graph()