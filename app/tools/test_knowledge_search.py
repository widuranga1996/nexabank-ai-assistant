from app.tools.knowledge_search import knowledge_search


def run_test(query: str):

    print("\n")
    print("=" * 70)
    print(f"QUERY: {query}")
    print("=" * 70)

    results = knowledge_search.search(
        query=query,
        role="Analyst",
        top_k=5,
    )

    for index, result in enumerate(results, 1):

        print(f"\n#{index}")

        print(
            f"Document: "
            f"{result['document_id']}"
        )

        print(
            f"Title: "
            f"{result['title']}"
        )

        print(
            f"Method: "
            f"{result.get('retrieval_method', 'sparse')}"
        )

        print(
            f"Sparse Score: "
            f"{result.get('sparse_score', 'N/A')}"
        )

        print(
            f"Dense Score: "
            f"{result.get('dense_score', 'N/A')}"
        )

        print(
            f"Hybrid Score: "
            f"{result.get('hybrid_score', 'N/A')}"
        )

        print(
            f"Type: "
            f"{result['document_type']}"
        )

        print(
            f"Department: "
            f"{result['department']}"
        )

        print(
            f"Content: "
            f"{result['content']}"
        )


if __name__ == "__main__":

    run_test(
        "payment failures caused by database connection problems"
    )

    run_test(
        "how do I troubleshoot payment gateway latency"
    )

    run_test(
        "payment timeout configuration"
    )