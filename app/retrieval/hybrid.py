def normalize_scores(results: list[dict]) -> list[dict]:

    if not results:
        return results

    scores = [
        result["score"]
        for result in results
    ]

    minimum = min(scores)
    maximum = max(scores)

    if maximum == minimum:

        for result in results:
            result["normalized_score"] = 1.0

        return results

    for result in results:

        result["normalized_score"] = (
            result["score"] - minimum
        ) / (maximum - minimum)

    return results


def hybrid_rank(
    sparse_results: list[dict],
    dense_results: list[dict],
    top_k: int = 5,
) -> list[dict]:

    sparse_results = normalize_scores(
        sparse_results
    )

    dense_results = normalize_scores(
        dense_results
    )

    combined = {}

    # -----------------------------------------
    # Sparse / BM25
    # -----------------------------------------

    for result in sparse_results:

        document_id = result["document_id"]

        combined.setdefault(
            document_id,
            {
                **result,
                "sparse_score": 0.0,
                "dense_score": 0.0,
            },
        )

        combined[document_id][
            "sparse_score"
        ] = result["normalized_score"]

    # -----------------------------------------
    # Dense / Pinecone
    # -----------------------------------------

    for result in dense_results:

        document_id = result["document_id"]

        combined.setdefault(
            document_id,
            {
                **result,
                "sparse_score": 0.0,
                "dense_score": 0.0,
            },
        )

        combined[document_id][
            "dense_score"
        ] = result["normalized_score"]

    # -----------------------------------------
    # Hybrid score
    # -----------------------------------------

    for result in combined.values():

        result["hybrid_score"] = (
            0.4 * result["sparse_score"]
            + 0.6 * result["dense_score"]
        )

        result["retrieval_method"] = "hybrid"

    # -----------------------------------------
    # Rank
    # -----------------------------------------

    ranked = sorted(
        combined.values(),
        key=lambda item: item["hybrid_score"],
        reverse=True,
    )

    return ranked[:top_k]