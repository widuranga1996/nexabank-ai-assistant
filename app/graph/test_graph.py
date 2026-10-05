import asyncio

from langchain_core.messages import HumanMessage

from app.graph.workflow import graph


async def main():

    result = await graph.ainvoke(
        {
            "messages": [
                HumanMessage(
                    content="What is the payment gateway troubleshooting procedure?"
                )
            ],
            "user_id": "user001",
            "role": "Analyst",
            "intent": "",
            "plan": [],
            "documents": [],
            "evidence": [],
            "analysis": {},
            "tool_results": [],
            "citations": [],
            "security_flags": [],
            "current_node": "",
            "final_answer": "",
        }
    )

    print(result)


asyncio.run(main())