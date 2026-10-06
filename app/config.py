import os

from dotenv import load_dotenv


load_dotenv()


OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY"
)

PINECONE_API_KEY = os.getenv(
    "PINECONE_API_KEY"
)

PINECONE_INDEX_NAME = os.getenv(
    "PINECONE_INDEX_NAME",
    "nexabank-knowledge",
)

LANGCHAIN_API_KEY = os.getenv(
    "LANGCHAIN_API_KEY"
)

LANGCHAIN_TRACING_V2 = os.getenv(
    "LANGCHAIN_TRACING_V2",
    "true",
)

LANGCHAIN_PROJECT = os.getenv(
    "LANGCHAIN_PROJECT",
    "nexabank-ai-assistant",
)