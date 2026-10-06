# NexaBank Enterprise AI Assistant — Architecture

## 1. High-Level Architecture

```mermaid
flowchart TB

    USER[User]

    UI[Streamlit Frontend]

    API[FastAPI Backend]

    AUTH[Authentication / RBAC]
    RATE[Token Bucket Rate Limiting]
    SECURITY[Security Guardrails]

    GRAPH[LangGraph Orchestrator]

    SUP[Supervisor Agent]

    RET[Knowledge Retrieval Agent]
    RES[Research / RLM Agent]
    RESP[Response Agent]
    VAL[Response Validator]

    HYBRID[Hybrid Retrieval]

    BM25[BM25 Sparse Search]
    PINE[Pinecone Dense Search]

    OPENAI[OpenAI LLM]
    EMB[OpenAI Embeddings]

    PYTHON[Python Analysis Tool]
    MCP[MCP Enterprise Tools]

    DOCS[Enterprise Documents]
    MEMORY[Conversation Memory]

    LS[LangSmith Observability]

    USER --> UI
    UI --> API

    API --> AUTH
    AUTH --> RATE
    RATE --> SECURITY

    SECURITY --> GRAPH

    GRAPH --> SUP

    SUP --> RET
    SUP --> RES
    SUP --> RESP

    RET --> HYBRID
    RES --> HYBRID

    HYBRID --> BM25
    HYBRID --> PINE

    BM25 --> DOCS
    PINE --> DOCS

    RES --> PYTHON
    RES --> MCP

    GRAPH --> MEMORY

    SUP --> OPENAI
    RES --> OPENAI
    RESP --> OPENAI

    PINE --> EMB

    RES --> RESP
    RET --> RESP

    RESP --> VAL

    GRAPH -. tracing .-> LS
    API -. tracing .-> LS
    HYBRID -. retrieval traces .-> LS
    MCP -. tool traces .-> LS