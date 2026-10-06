import time
import httpx
import streamlit as st


API_URL = "http://127.0.0.1:8000/api/chat"


st.set_page_config(
    page_title="NexaBank AI Assistant",
    page_icon="🏦",
    layout="wide",
)


# ---------------------------------------------------------
# Session state
# ---------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "activity_log" not in st.session_state:
    st.session_state.activity_log = []


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.title("🏦 NexaBank AI Assistant")
st.caption(
    "Enterprise AI Assistant • LangGraph • Hybrid RAG • "
    "Pinecone • LangSmith"
)


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:
    st.header("Assistant")

    user_id = st.selectbox(
        "User",
        [
            "user001",
            "user002",
            "admin001",
        ],
    )

    user_labels = {
        "user001": "Viewer",
        "user002": "Analyst",
        "admin001": "Administrator",
    }

    st.caption(f"Role: **{user_labels[user_id]}**")

    st.divider()

    st.subheader("System")

    st.success("FastAPI: Connected")

    st.write("**Architecture**")
    st.write("• LangGraph")
    st.write("• Hybrid RAG")
    st.write("• Pinecone")
    st.write("• BM25")
    st.write("• LangSmith")

    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.session_state.activity_log = []
        st.rerun()


# ---------------------------------------------------------
# Main layout
# ---------------------------------------------------------

chat_column, activity_column = st.columns([2.5, 1])


# ---------------------------------------------------------
# Chat
# ---------------------------------------------------------

with chat_column:

    st.subheader("Conversation")

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if message["role"] == "assistant":

                citations = message.get("citations", [])

                if citations:
                    st.caption(
                        "Sources: "
                        + ", ".join(citations)
                    )

    prompt = st.chat_input(
        "Ask NexaBank AI about enterprise knowledge..."
    )

    if prompt:

        # Display user message immediately
        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        # Call backend
        with st.chat_message("assistant"):

            with st.spinner("Processing request..."):

                try:

                    response = httpx.post(
                        API_URL,
                        json={
                            "user_id": user_id,
                            "message": prompt,
                        },
                        timeout=120.0,
                    )

                    response.raise_for_status()

                    data = response.json()

                    answer = data.get(
                        "answer",
                        "No response generated.",
                    )

                    citations = data.get(
                        "citations",
                        [],
                    )

                    activity_log = data.get(
                        "activity_log",
                        [],
                    )

                    security_flags = data.get(
                        "security_flags",
                        [],
                    )

                    # Save activity
                    st.session_state.activity_log = activity_log

                    # Display response
                    st.markdown(answer)

                    if citations:
                        st.caption(
                            "Sources: "
                            + ", ".join(citations)
                        )

                    if security_flags:
                        st.warning(
                            "Security flags detected: "
                            + ", ".join(security_flags)
                        )

                    # Save assistant response
                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer,
                            "citations": citations,
                        }
                    )

                except httpx.HTTPStatusError as exc:

                    st.error(
                        f"Backend returned HTTP "
                        f"{exc.response.status_code}"
                    )

                except Exception as exc:

                    st.error(
                        f"Unable to contact the backend: {exc}"
                    )


# ---------------------------------------------------------
# Agent Activity Panel
# ---------------------------------------------------------

with activity_column:

    st.subheader("🔎 Agent Activity")

    if not st.session_state.activity_log:

        st.info(
            "Agent activity will appear here "
            "after a request."
        )

    else:

        for activity in st.session_state.activity_log:

            node = activity.get(
                "node",
                "unknown",
            )

            status = activity.get(
                "status",
                "",
            )

            message = activity.get(
                "message",
                "",
            )

            if status == "passed":
                icon = "✅"

            elif status == "blocked":
                icon = "🚫"

            elif status == "tool_call":
                icon = "🔧"

            elif status == "running":
                icon = "🔄"

            elif status == "completed":
                icon = "✅"

            else:
                icon = "ℹ️"

            st.markdown(
                f"{icon} **{node}**  \n"
                f"<small>{message}</small>",
                unsafe_allow_html=True,
            )

            st.divider()