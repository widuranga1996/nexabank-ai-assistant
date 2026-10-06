from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

    user_id: str
    role: str

    intent: str
    plan: list

    documents: list
    evidence: list

    analysis: dict
    tool_results: list

    citations: list
    security_flags: list
    activity_log: list

    research_results: list
    research_depth: int

    current_node: str
    final_answer: str
    
# class AgentState(TypedDict):
#     messages: Annotated[list, add_messages]

#     user_id: str
#     role: str

#     intent: str
#     plan: list

#     documents: list
#     evidence: list

#     analysis: dict
#     tool_results: list

#     citations: list
#     security_flags: list

#     activity_log: list

#     current_node: str
#     final_answer: str