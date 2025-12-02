""" Service Gateway for the Inferencing API. """
import logging
import json
import re
import streamlit as st
from openai import OpenAI
from utils.settings import settings

logger = logging.getLogger(__name__)

# pylint: disable=too-few-public-methods
class InferenceGateway():
    """ OpenAI Service Gateway """

    MAX_RETRIES = 3

    # openai client
    openai_client : OpenAI = None

    def __init__(self):
        """ Default Constructor """
        self.openai_client = OpenAI(base_url=settings.OPENAI_BASE_URL,
                                    api_key=settings.OPENAI_API_KEY)

    def simple_chat(self, model, system_prompt, user_prompt, mcp_list: list[dict] = []):
        """ Executes a simple chat based on the provided prompts.

            model - model to use
            system_prompt - system prompt
            user_prompt - user prompt
            mcp_list - list of tools
        """
        # validate required fields
        if user_prompt is None or len(user_prompt) == 0:
            msg = "User Prompt is a required field and cannot be empty!"
            logger.error(msg)
            raise ValueError(msg)

        # soften optional fields
        if system_prompt is not None and len(system_prompt) == 0:
            logger.debug("Softening system_prompt")
            system_prompt = None

        # Employ OpenAI Responses AI
        response = self.openai_client.responses.create(
            model=model,
            instructions=system_prompt,
            input=user_prompt,
            tools=mcp_list,
            temperature=0.3,
            max_output_tokens=2048,
            top_p=1,
            store=True,
            previous_response_id=None,
            parallel_tool_calls=True,
            stream=False,
        )
        response = response.output_text
        logger.debug("AI Response: %s", response)

        return response


    def streaming_chat(self, model: str, system_prompt: str, user_input: str, mcp_list: list[dict], placeholder, previous_response_id=None) -> str:
        """ Process a chat request.
        
            user_input - user message
            placeholder - streamlit placeholder
            
            Returns: Chat response
        """
        logger.info("MCP Server List: %s", mcp_list)

        # Employ OpenAI Responses AI
        response_stream = self.openai_client.responses.create(
            model=model,
            instructions=system_prompt,
            input=user_input,
            tools=mcp_list,
            temperature=0.3,
            max_output_tokens=2048,
            top_p=1,
            store=True,
            previous_response_id=previous_response_id,
            parallel_tool_calls=True,
            stream=True,
        )

        # Capture response
        ai_response = ""
        for event in response_stream:
            logger.info("Event: %s", event)
            if hasattr(event, "type") and "text.delta" in event.type:
                ai_response += event.delta
                with placeholder.container():
                    st.write(ai_response)
            elif hasattr(event, "type") and "response.completed" in event.type:
                self.previous_response_id = event.response.id

        return ai_response

    def json_chat(self, model, system_prompt, user_prompt, tools = []):
        """ Executes a simple chat based on the provided prompts that responds in JSON

            model - model to use
            system_prompt - system prompt
            user_prompt - user prompt
            tools - tools to use
        """
        # validate required fields
        if user_prompt is None or len(user_prompt) == 0:
            msg = "User Prompt is a required field and cannot be empty!"
            logger.error(msg)
            raise ValueError(msg)

        # soften optional fields
        if system_prompt is not None and len(system_prompt) == 0:
            logger.debug("Softening system_prompt")
            system_prompt = None

        retry_count = 0
        while retry_count < self.MAX_RETRIES:
            # Employ OpenAI Responses AI
            response = self.openai_client.responses.create(
                model=model,
                instructions=system_prompt,
                input=user_prompt,
                tools=tools,
                temperature=0.3,
                max_output_tokens=2048,
                top_p=1,
                store=False,
                parallel_tool_calls=True,
                stream=False,
            )
            ai_response = response.output_text
            logger.info("Original AI Response: %s", ai_response)

            # remove leading text, if existent
            ai_response = re.sub(r"^analysis.*final{", "{", ai_response.strip(), flags=re.IGNORECASE|re.DOTALL)
            ai_response = ai_response.strip().removeprefix("```")
            ai_response = ai_response.strip().removeprefix("final")
            ai_response = ai_response.strip().removeprefix("json")
            ai_response = ai_response.strip().removesuffix("```")
            print("JSON as Text Before Parsing:\n" + ai_response)
            try:
                return json.loads(ai_response)
            except json.JSONDecodeError as e:
                logger.error("AI returned invalid JSON.  Retrying...  Error=%s. Response=%s", e, ai_response)
            
            retry_count += 1

        # raise error
        msg = "AI was unable to create parsable JSON after several attempts.  Failing operation."
        logger.error(msg)
        raise ValueError(msg)
