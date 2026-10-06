import os

from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings

load_dotenv()


INDEX_NAME = os.getenv(
    "PINECONE_INDEX_NAME",
    "nexabank-knowledge",
)

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")


embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)


pc = Pinecone(
    api_key=PINECONE_API_KEY
)


def ensure_index():

    existing_indexes = [
        index["name"]
        for index in pc.list_indexes()
    ]

    if INDEX_NAME not in existing_indexes:

        pc.create_index(
            name=INDEX_NAME,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1",
            ),
        )

    return pc.Index(INDEX_NAME)