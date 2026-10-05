from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage


load_dotenv()


model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


async def supervisor_node(state):

    messages = [
        SystemMessage(
            content="""
You are the Supervisor Agent for NexaBank AI Assistant.

Your responsibility is to classify the user's request.

Choose exactly ONE intent:

1. knowledge_retrieval
   - Questions answerable from company documents.

2. research
   - Complex questions requiring investigation across
     multiple documents or multiple steps.

3. analytics
   - Questions requiring calculations, aggregation,
     statistics, or structured analysis.

4. direct_response
   - General conversational questions that do not
     require company knowledge.

Return ONLY the intent name.
"""
        ),
        *state["messages"],
    ]

    response = await model.ainvoke(messages)

    intent = response.content.strip().lower()

    valid_intents = {
        "knowledge_retrieval",
        "research",
        "analytics",
        "direct_response",
    }

    if intent not in valid_intents:
        intent = "knowledge_retrieval"

    state["intent"] = intent
    state["current_node"] = "supervisor"

    return state