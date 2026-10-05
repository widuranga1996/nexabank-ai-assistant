async def validation_node(state):
    """
    Validate the generated response before returning it
    to the user.
    """

    state["current_node"] = "validator"

    state.setdefault("activity_log", [])

    answer = state.get("final_answer", "")
    citations = state.get("citations", [])
    evidence = state.get("evidence", [])

    valid_document_ids = {
        item["document_id"]
        for item in evidence
    }

    invalid_citations = [
        citation
        for citation in citations
        if citation not in valid_document_ids
    ]

    validation_errors = []

    if not answer.strip():
        validation_errors.append(
            "Response is empty."
        )

    if invalid_citations:
        validation_errors.append(
            f"Invalid citations: {invalid_citations}"
        )

    if validation_errors:

        state["security_flags"] = validation_errors

        state["final_answer"] = (
            "I was unable to produce a validated answer "
            "from the available evidence."
        )

        state["activity_log"].append(
            {
                "node": "validator",
                "status": "failed",
                "message": "; ".join(validation_errors),
            }
        )

    else:

        state["activity_log"].append(
            {
                "node": "validator",
                "status": "passed",
                "message": "Response and citations validated",
            }
        )

    return state