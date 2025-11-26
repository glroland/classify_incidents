""" Automation Playground Component """
import logging
import requests
import streamlit as st
from gateways.inference_gateway import InferenceGateway
from utils.settings import settings

logger = logging.getLogger(__name__)

def get_mcp_servers_list(allowed_tools):
    """ Dynamically generate MCP Server Tool for OpenAI Responses API
    
        allowed_tools - list of allowed tool calls within MCP server

        Returns: list of MCP Servers
    """
    mcp_servers_list = []

    if allowed_tools is None or len(allowed_tools) == 0:
        mcp_servers_list.append(
            # Automate IT Agent
            {
                "type": "mcp",
                "server_label": "automate-agent",
                "server_url": settings.AUTOMATE_AGENT_URL,
                "require_approval": "never",
            }
        )
    else:
        mcp_servers_list.append(
            # Automate IT Agent
            {
                "type": "mcp",
                "server_label": "automate-agent",
                "server_url": settings.AUTOMATE_AGENT_URL,
                "require_approval": "never",
                "allowed_tools": allowed_tools,
            }
        )

    #research_request
    #create_plan
    #judge_plan
    #write_ansible_playbook
    #write_bash_script
    #write_powershell_script
    #validate_code

    return mcp_servers_list


def invoke_api(api_name, query_parameters):
    url = settings.AUTOMATE_AGENT_API_URL + "/" + api_name
    http_response = requests.get(url, params=query_parameters, timeout=settings.API_TIMEOUT)
    if http_response.status_code != 200:
            msg = f"Unable to invoke Automation Agent API.  HTTP Response Code = {http_response.status_code}"
            logger.error(msg)
            raise ValueError(msg)
    data = http_response.text
    logging.info("API Invoke Response: '%s'", data)
    return data


def handle_user_input(prompt: str, placeholder):
    """ Processes a user prompt.
    
        prompt - user request
        placeholder - streamlit placeholder widget
    """
    gateway = InferenceGateway()

    # Research Request
    placeholder.text("Researching request...")
    query_parameters = {
        "user_request": prompt,
    }
    research = invoke_api("research_request", query_parameters)
    with st.expander("See research"):
        st.markdown(research)

    # Create Implementation Plan
    placeholder.text("Research complete.  Creating implementation plan...")
    query_parameters = {
        "user_request": prompt,
        "research": research,
    }
    nominated_plan = invoke_api("create_plan", query_parameters)
    with st.expander("See implementation plan"):
        st.markdown(nominated_plan)

    # Judge Implementation Plan
    placeholder.text("Implementation plan created.  Obtaining a peer review from a judge...")
    query_parameters = {
        "user_request": prompt,
        "research": research,
        "nominated_plan": nominated_plan,
    }
    feedback_on_plan = invoke_api("judge_plan", query_parameters)
    with st.expander("See feedback on plan after AI review"):
        st.markdown(feedback_on_plan)

    # Judge Implementation Plan
    placeholder.text("Writing Bash script based on the final implementation plan...")
    query_parameters = {
        "plan": nominated_plan,
    }
    source_code = invoke_api("write_bash_script", query_parameters)
    st.code(source_code, language="bash", line_numbers=True)

    # Validate Source Code
    placeholder.text("Performing a code review of the generated source code...")
    query_parameters = {
        "language": "bash",
        "source_code": source_code,
    }
    code_review_feedback = invoke_api("validate_code", query_parameters)
    with st.expander("See code review feedback"):
        st.code(code_review_feedback, language=None)

    placeholder.markdown(":green[*Completed Successfully!*]")


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
        handle_user_input(prompt, placeholder)
