""" Automation Playground Component """
import logging
import streamlit as st
from commands.create_generic_automation import CreateGenericAutomationCommand

logger = logging.getLogger(__name__)

def update_status_callback(placeholder, msg: str):
    placeholder.markdown(msg)

def output_markdown_callback(msg: str, markdown: str):
    with st.expander(msg):
        st.markdown(markdown)

def output_code_callback(msg: str, code: str):
    with st.expander(msg):
        st.code(code, language=None)

def artifact_created_callback(language: str, source_code: str):
    st.code(source_code,
            language=language,
            line_numbers=True)

def playground():
    st.title("Automation Playground")

    # Initialize chat experience on first run
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Describe what you would like to automate."):
        # Display user message in chat message container
        with st.chat_message("user"):
            # Add user message to chat history
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Create response
        with st.chat_message("assistant"):
            placeholder = st.empty()
        command = CreateGenericAutomationCommand()
        command.prompt = prompt
        command.placeholder = placeholder
        command.fn_update_status = update_status_callback
        command.fn_output_markdown = output_markdown_callback
        command.fn_output_code = output_code_callback
        command.fn_artifact = artifact_created_callback
        command.go()

        # Display each artifact
        for artifact in command.artifacts:
            st.download_button(
                label=f"Download {artifact.filename}",
                data=artifact.source_code,
                file_name=artifact.filename,
                on_click="ignore",
                type="primary",
                icon=":material/download:",
            )
