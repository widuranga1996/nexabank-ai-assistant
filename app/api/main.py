from fastapi import FastAPI, HTTPException
from langchain_core.messages import HumanMessage

from app.api.models import ChatRequest, ChatResponse
from app.graph.workflow import graph
from app.security.rbac import get_role


app = FastAPI(
    title="NexaBank Enterprise AI Assistant",
    version="1.0.0",
)


@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "service": "nexabank-ai-assistant"
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):

    role = get_role(request.user_id)

    if not role:
        raise HTTPException(
            status_code=401,
            detail="Unknown user"
        )

    try:
        result = await graph.ainvoke(
            {
                "messages": [
                    HumanMessage(content=request.message)
                ],
                "user_id": request.user_id,
                "role": role,
                "activity_log": [],
            },
            config={
                "tags": ["nexabank", "production-poc"],
                "metadata": {
                    "user_id": request.user_id,
                    "role": role,
                    "interface": "fastapi",
                },
            },
        )

        return ChatResponse(
            answer=result.get("final_answer", ""),
            intent=result.get("intent", ""),
            citations=result.get("citations", []),
            security_flags=result.get("security_flags", []),
            activity_log=result.get("activity_log", []),
            analysis=result.get("analysis", {}),
        )

    except Exception as exc:
        print(f"Chat error: {exc}")

        raise HTTPException(
            status_code=500,
            detail="The assistant encountered an internal processing error."
        )