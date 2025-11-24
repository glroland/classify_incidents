""" Automation Playground Component """
import streamlit as st
from gateways.inference_gateway import InferenceGateway
from utils.settings import settings

MCP_SERVERS_LIST = [
    # Automate IT Agent
    {
        "type": "mcp",
        "server_label": "automate-agent",
        "server_url": settings.AUTOMATE_AGENT_URL,
        "require_approval": "never"
    }
]

def playground():
    st.title("Automation Playground")

    # Initialize chat experience on first run
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    gateway = InferenceGateway()

    if prompt := st.chat_input("Describe what you would like to automate."):
        # Display user message in chat message container
        with st.chat_message("user"):
            # Add user message to chat history
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Create response
        with st.chat_message("assistant"):
            placeholder = st.empty()
        ai_response = gateway.streaming_chat(
                model=settings.OPENAI_MODEL,
                system_prompt="",
                user_input=prompt,
                mcp_list=MCP_SERVERS_LIST,
                placeholder=placeholder,
                previous_response_id=None)

        # Add user message to chat history
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
