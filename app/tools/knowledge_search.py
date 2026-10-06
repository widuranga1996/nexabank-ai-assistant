import bm25s

from app.retrieval.document_loader import load_documents
from app.retrieval.dense_search import dense_search
from app.retrieval.hybrid import hybrid_rank


def build_search_corpus(documents: list[dict]) -> list[str]:
    corpus = []

    for document in documents:
        text = " ".join(
            [
                document.get("title", ""),
                document.get("content", ""),
                document.get("root_cause", ""),
                document.get("department", ""),
                document.get("document_type", ""),
            ]
        )

        corpus.append(text)

    return corpus


class KnowledgeSearch:

    def __init__(self):
        self.documents = load_documents()

        corpus = build_search_corpus(
            self.documents
        )

        self.tokenized_corpus = bm25s.tokenize(
            corpus,
            stopwords="en",
        )

        self.retriever = bm25s.BM25()

        self.retriever.index(
            self.tokenized_corpus
        )

    # ==================================================
    # Sparse BM25 Search
    # ==================================================

    def _sparse_search(
        self,
        query: str,
        role: str,
        top_k: int = 5,
        document_type: str | None = None,
        department: str | None = None,
    ) -> list[dict]:

        query_tokens = bm25s.tokenize(
            [query],
            stopwords="en",
        )

        top_k = max(
            1,
            min(top_k, len(self.documents)),
        )

        search_k = min(
            top_k * 2,
            len(self.documents),
        )

        results, scores = self.retriever.retrieve(
            query_tokens,
            k=search_k,
        )

        output = []

        for index, score in zip(
            results[0],
            scores[0],
        ):

            document = self.documents[int(index)]

            # ------------------------------------------
            # RBAC
            # ------------------------------------------

            if document.get("access_level") == "restricted":

                if role != "Administrator":
                    continue

            # ------------------------------------------
            # Metadata filters
            # ------------------------------------------

            if document_type:

                if document.get("document_type") != document_type:
                    continue

            if department:

                if document.get("department") != department:
                    continue

            # ------------------------------------------
            # Search result
            # ------------------------------------------

            output.append(
                {
                    "document_id": document.get("id"),
                    "title": document.get("title"),
                    "content": document.get("content"),
                    "root_cause": document.get("root_cause"),
                    "document_type": document.get(
                        "document_type"
                    ),
                    "department": document.get(
                        "department"
                    ),
                    "created_date": document.get(
                        "created_date"
                    ),
                    "score": float(score),
                }
            )

            if len(output) >= top_k:
                break

        return output

    # ==================================================
    # Hybrid Knowledge Search
    # ==================================================

    def search(
        self,
        query: str,
        role: str,
        top_k: int = 5,
        document_type: str | None = None,
        department: str | None = None,
    ) -> list[dict]:

        # ------------------------------------------
        # 1. Sparse BM25 retrieval
        # ------------------------------------------

        sparse_results = self._sparse_search(
            query=query,
            role=role,
            top_k=top_k,
            document_type=document_type,
            department=department,
        )

        # ------------------------------------------
        # 2. Dense Pinecone retrieval
        # ------------------------------------------

        try:

            dense_results = dense_search(
                query=query,
                role=role,
                top_k=top_k,
                document_type=document_type,
                department=department,
            )

            # ------------------------------------------
            # 3. Hybrid ranking
            # ------------------------------------------

            hybrid_results = hybrid_rank(
                sparse_results,
                dense_results,
                top_k=top_k,
            )

            return hybrid_results

        # ------------------------------------------
        # 4. Graceful fallback
        # ------------------------------------------

        except Exception as exc:

            print(
                f"Dense retrieval unavailable: {exc}"
            )

            return sparse_results[:top_k]


knowledge_search = KnowledgeSearch()