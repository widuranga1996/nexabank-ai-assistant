from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

# from app.agents.retrieval import load_documents
from app.tools.knowledge_search import knowledge_search
from app.tools.analysis import (
    analyze_incident_batch,
    aggregate_batch_results,
)

load_dotenv()


model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)


async def research_node(state):
    """
    RLM-style Research Agent.

    The agent does not place the entire document collection
    into the LLM context.

    Instead it:

    1. Creates a research plan.
    2. Explores the document collection.
    3. Retrieves targeted documents.
    4. Splits documents into batches.
    5. Analyzes batches independently.
    6. Aggregates the results.
    """

    state["current_node"] = "research"

    state.setdefault("activity_log", [])

    state["activity_log"].append(
        {
            "node": "research",
            "status": "started",
            "message": "Starting recursive research",
        }
    )

    # ------------------------------------------------
    # Step 1: Research plan
    # ------------------------------------------------

    state["plan"] = [
        "Find payment-related incident reports",
        "Filter incidents to the requested period",
        "Split incidents into analysis batches",
        "Analyze recurring root causes",
        "Aggregate batch findings",
        "Find supporting operational runbooks",
    ]

    state["activity_log"].append(
        {
            "node": "research",
            "status": "completed",
            "message": "Research plan created",
        }
    )

    # ------------------------------------------------
    # Step 2: Explore document collection
    # ------------------------------------------------

    # all_documents = load_documents()

    # payment_incidents = [
    #     document
    #     for document in all_documents
    #     if (
    #         document.get("document_type") == "incident"
    #         and document.get("department") == "payments"
    #     )
    # ]
    search_results = knowledge_search.search(
        query="payment failures payment incidents",
        role=state.get("role", "Viewer"),
        top_k=10,
        document_type="incident",
        department="payments",
    )

    payment_incidents = search_results
    # ------------------------------------------------
    # Step 3: Batch decomposition
    # ------------------------------------------------

    batch_size = 2

    batches = [
        payment_incidents[i:i + batch_size]
        for i in range(
            0,
            len(payment_incidents),
            batch_size,
        )
    ]

    state["research_depth"] = len(batches)

    state["activity_log"].append(
        {
            "node": "research",
            "status": "completed",
            "message": (
                f"Found {len(payment_incidents)} payment incidents "
                f"and created {len(batches)} research batches"
            ),
        }
    )

    state["activity_log"].append(
        {
            "node": "research",
            "status": "tool_call",
            "message": "Knowledge Search: payment incidents",
        }
    )
    # ------------------------------------------------
    # Step 4: Recursive batch analysis
    # ------------------------------------------------

    batch_results = []

    for index, batch in enumerate(batches):

        state["activity_log"].append(
            {
                "node": "research",
                "status": "running",
                "message": (
                    f"Analyzing research batch "
                    f"{index + 1}/{len(batches)}"
                ),
            }
        )

        result = analyze_incident_batch(batch)

        batch_results.append(result)

    # ------------------------------------------------
    # Step 5: Aggregate results
    # ------------------------------------------------

    aggregate = aggregate_batch_results(
        batch_results
    )

    state["analysis"] = aggregate

    # Preserve the documents as evidence.
    state["documents"] = payment_incidents

    # state["evidence"] = [
    #     {
    #         "document_id": document["id"],
    #         "title": document["title"],
    #         "content": document["content"],
    #         "score": 1.0,
    #     }
    #     for document in payment_incidents
    # ]
    state["evidence"] = [
        {
            "document_id": document["document_id"],
            "title": document["title"],
            "content": document["content"],
            "score": document["score"],
        }
        for document in payment_incidents
    ]

    state["research_results"] = batch_results

    state["activity_log"].append(
        {
            "node": "research",
            "status": "completed",
            "message": (
                f"Research completed. "
                f"{aggregate['total_incidents']} incidents analyzed."
            ),
        }
    )

    return state