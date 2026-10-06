from app.retrieval.pinecone_store import (
    ensure_index,
    embeddings,
)


def dense_search(
    query: str,
    role: str,
    top_k: int = 5,
    document_type: str | None = None,
    department: str | None = None,
):

    index = ensure_index()

    query_vector = embeddings.embed_query(
        query
    )

    filters = {}

    if document_type:
        filters["document_type"] = document_type

    if department:
        filters["department"] = department

    if role != "Administrator":
        filters["access_level"] = {
            "$ne": "restricted"
        }

    response = index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True,
        namespace="enterprise",
        filter=filters if filters else None,
    )

    results = []

    for match in response.matches:

        metadata = match.metadata or {}

        results.append(
            {
                "document_id": metadata.get(
                    "document_id"
                ),
                "title": metadata.get(
                    "title"
                ),
                "content": metadata.get(
                    "content"
                ),
                "root_cause": metadata.get(
                    "root_cause"
                ),
                "document_type": metadata.get(
                    "document_type"
                ),
                "department": metadata.get(
                    "department"
                ),
                "created_date": metadata.get(
                    "created_date"
                ),
                "score": float(
                    match.score
                ),
            }
        )

    return results