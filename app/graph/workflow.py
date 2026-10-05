from langgraph.graph import StateGraph, START, END

from app.graph.state import AgentState
from app.graph.router import route_from_supervisor
from app.agents.supervisor import supervisor_node


async def knowledge_retrieval_node(state: AgentState):
    state["current_node"] = "knowledge_retrieval"
    return state


async def research_node(state: AgentState):
    state["current_node"] = "research"
    return state


async def analytics_node(state: AgentState):
    state["current_node"] = "analytics"
    return state


async def direct_response_node(state: AgentState):
    state["current_node"] = "direct_response"
    return state


def build_graph():

    graph = StateGraph(AgentState)

    # Nodes
    graph.add_node(
        "supervisor",
        supervisor_node,
    )

    graph.add_node(
        "knowledge_retrieval",
        knowledge_retrieval_node,
    )

    graph.add_node(
        "research",
        research_node,
    )

    graph.add_node(
        "analytics",
        analytics_node,
    )

    graph.add_node(
        "direct_response",
        direct_response_node,
    )

    # START → Supervisor
    graph.add_edge(
        START,
        "supervisor",
    )

    # Supervisor → Router → Specialized Agent
    graph.add_conditional_edges(
        "supervisor",
        route_from_supervisor,
        {
            "knowledge_retrieval": "knowledge_retrieval",
            "research": "research",
            "analytics": "analytics",
            "direct_response": "direct_response",
        },
    )

    # Specialized agents → END
    graph.add_edge(
        "knowledge_retrieval",
        END,
    )

    graph.add_edge(
        "research",
        END,
    )

    graph.add_edge(
        "analytics",
        END,
    )

    graph.add_edge(
        "direct_response",
        END,
    )

    return graph.compile()


graph = build_graph()