from app.graph.state import AgentState
from app.tools.knowledge_search import knowledge_search


async def retrieval_node(state: AgentState):

    state["current_node"] = "retrieval"

    state.setdefault("activity_log", [])

    state["activity_log"].append(
        {
            "node": "retrieval",
            "status": "started",
            "message": "Searching enterprise knowledge",
        }
    )

    query = state["messages"][-1].content

    role = state.get("role", "Viewer")

    results = knowledge_search.search(
        query=query,
        role=role,
        top_k=5,
    )

    state["documents"] = [
        result
        for result in results
    ]

    state["evidence"] = [
        {
            "document_id": result["document_id"],
            "title": result["title"],
            "content": result["content"],
            "score": result["score"],
        }
        for result in results
    ]

    state["tool_results"] = [
        {
            "tool": "knowledge_search",
            "result_count": len(results),
        }
    ]

    state["activity_log"].append(
        {
            "node": "retrieval",
            "status": "completed",
            "message": f"Retrieved {len(results)} supporting documents",
        }
    )

    return state