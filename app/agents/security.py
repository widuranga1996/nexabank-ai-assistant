from app.graph.state import AgentState
from app.security.guard import security_check


async def security_node(
    state: AgentState,
):
    state["current_node"] = "security"

    state.setdefault(
        "activity_log",
        [],
    )

    user_id = state.get("user_id", "")
    query = state["messages"][-1].content

    result = security_check(
        user_id=user_id,
        query=query,
    )

    state["security_flags"] = result["flags"]

    if result["allowed"]:

        state["activity_log"].append(
            {
                "node": "security",
                "status": "passed",
                "message": "Security checks passed",
            }
        )

    else:

        state["activity_log"].append(
            {
                "node": "security",
                "status": "blocked",
                "message": "Request blocked by security guard",
            }
        )

        state["final_answer"] = (
            "I’m unable to process this request "
            "because it violates the assistant's "
            "security policies."
        )

    return state