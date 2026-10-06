# 🏦 NexaBank Enterprise AI Assistant

An enterprise-oriented AI assistant for querying organizational documents, investigating incidents, performing structured research, and producing evidence-grounded responses.

The system combines **LangGraph agent orchestration, Hybrid RAG, Pinecone, BM25, RLM-style research, Python analysis, RBAC, security guardrails, FastAPI, Streamlit, and LangSmith observability**.

---

# 1. Problem Statement

Enterprise organizations maintain large collections of operational documents including:

- Incident reports
- Architecture documentation
- Runbooks
- Policies
- Service information
- Operational knowledge

Traditional keyword search is insufficient for complex questions that require:

1. Finding relevant documents
2. Understanding relationships between documents
3. Decomposing a complex research question
4. Performing analysis across multiple documents
5. Identifying recurring patterns
6. Providing evidence-backed answers

NexaBank AI Assistant addresses this problem using a controlled multi-agent architecture.

---

# 2. Key Capabilities

## AI Agent Architecture

The system uses LangGraph to orchestrate specialized components:

- Security Agent
- Supervisor Agent
- Knowledge Retrieval Agent
- Research Agent
- Response Agent
- Validation Agent

## Hybrid RAG

Retrieval combines:

- BM25 sparse retrieval
- Pinecone dense vector retrieval
- Hybrid result ranking
- Metadata filtering
- Role-based document access

## RLM-Style Research

Complex questions are decomposed into smaller research tasks.

The Research Agent can:

- Generate a research plan
- Decompose a question
- Retrieve relevant documents
- Create analysis batches
- Execute Python analysis
- Aggregate findings
- Provide evidence to the response agent

## Security

The system includes:

- Input validation
- Prompt injection detection
- Role-based access control
- Tool authorization
- Restricted document protection
- Response validation

## Observability

LangSmith provides tracing for the AI workflow and enables investigation of:

- Agent execution
- LLM calls
- Retrieval
- Tool calls
- Agent transitions
- Errors

---

# 3. Architecture

```text
                         ┌──────────────────────┐
                         │      User            │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Streamlit UI       │
                         │ Chat + Activity      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      FastAPI         │
                         │ Validation / RBAC    │
                         │ Rate Limiting        │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Security Guard     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                    ┌──────────────────────────────┐
                    │       LangGraph              │
                    │                              │
                    │        Supervisor            │
                    │             │                │
                    │       ┌─────┴─────┐          │
                    │       ▼           ▼          │
                    │ Retrieval      Research      │
                    │                   │          │
                    │                   ▼          │
                    │             Python Analysis  │
                    │                   │          │
                    │                   ▼          │
                    │               Response       │
                    │                   │          │
                    │                   ▼          │
                    │               Validator      │
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────┼───────────────┐
                    ▼              ▼               ▼
                 BM25          Pinecone           MCP
                 Sparse          Dense          Enterprise
                Retrieval      Retrieval          Tools
                    │              │
                    └──────┬───────┘
                           ▼
                  Enterprise Documents

                           │
                           ▼
                     LangSmith
                    Observability