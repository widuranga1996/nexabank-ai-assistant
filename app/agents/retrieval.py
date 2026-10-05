import json
from pathlib import Path

from app.graph.state import AgentState


DATA_DIR = Path("data")


def load_documents() -> list[dict]:
    """
    Load enterprise knowledge documents from the local
    POC document store.

    This will later be replaced/augmented by Pinecone
    and BM25 retrieval.
    """

    documents = []

    for path in DATA_DIR.rglob("*.json"):
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, list):
                documents.extend(data)
            else:
                documents.append(data)

    return documents


def keyword_score(query: str, document: dict) -> int:
    """
    Very small deterministic keyword scorer for the initial POC.

    This is intentionally simple. The production retrieval
    layer will add dense embeddings and BM25.
    """

    query_words = set(query.lower().split())

    searchable_text = " ".join(
        [
            document.get("title", ""),
            document.get("content", ""),
            document.get("root_cause", ""),
        ]
    ).lower()

    return sum(
        1
        for word in query_words
        if len(word) > 3 and word in searchable_text
    )


async def retrieval_node(state: AgentState):
    """
    Retrieval Agent.

    Responsibilities:
    - Search enterprise documents
    - Apply basic relevance ranking
    - Return supporting evidence
    - Preserve document attribution
    """

    state["current_node"] = "retrieval"

    query = state["messages"][-1].content

    documents = load_documents()

    ranked_documents = []

    for document in documents:

        # Basic access control at retrieval level.
        if document.get("access_level") == "restricted":
            if state.get("role") != "Administrator":
                continue

        score = keyword_score(query, document)

        if score > 0:
            ranked_documents.append(
                {
                    "document": document,
                    "score": score,
                }
            )

    ranked_documents.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    top_results = ranked_documents[:5]

    state["documents"] = [
        item["document"]
        for item in top_results
    ]

    state["evidence"] = [
        {
            "document_id": item["document"]["id"],
            "title": item["document"]["title"],
            "content": item["document"]["content"],
            "score": item["score"],
        }
        for item in top_results
    ]

    return state