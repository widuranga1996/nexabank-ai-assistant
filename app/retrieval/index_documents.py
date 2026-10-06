# from app.agents.retrieval import load_documents
from app.retrieval.document_loader import load_documents
from app.retrieval.pinecone_store import (
    ensure_index,
    embeddings,
)


def build_text(document: dict) -> str:

    return " ".join(
        [
            document.get("title", ""),
            document.get("content", ""),
            document.get("root_cause", ""),
            document.get("department", ""),
            document.get("document_type", ""),
        ]
    )


def main():

    documents = load_documents()

    index = ensure_index()

    records = []

    for document in documents:

        document_id = document["id"]

        text = build_text(document)

        vector = embeddings.embed_query(text)

        metadata = {
            "document_id": document_id,
            "title": document.get("title", ""),
            "content": document.get("content", ""),
            "document_type": document.get(
                "document_type",
                "",
            ),
            "department": document.get(
                "department",
                "",
            ),
            "access_level": document.get(
                "access_level",
                "internal",
            ),
            "created_date": document.get(
                "created_date",
                "",
            ),
            "root_cause": document.get(
                "root_cause",
                "",
            ),
        }

        records.append(
            {
                "id": document_id,
                "values": vector,
                "metadata": metadata,
            }
        )

    index.upsert(
        vectors=records,
        namespace="enterprise",
    )

    print(
        f"Indexed {len(records)} documents "
        f"into Pinecone."
    )


if __name__ == "__main__":
    main()