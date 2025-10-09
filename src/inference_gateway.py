import os
import logging
from openai import OpenAI
from settings import settings

logger = logging.getLogger(__name__)

class InferenceGateway():
    """ OpenAI Service Gateway """

    # openai client
    openai_client : OpenAI = None

    def __init__(self):
        """ Default Constructor """
        self.openai_client = OpenAI(base_url=settings.OPENAI_BASE_URL,
                                    api_key=settings.OPENAI_API_KEY)

    def simple_chat(self, system_prompt, user_prompt):
        """ Executes a simple chat based on the provided prompts.

            system_prompt - system prompt
            user_prompt - user prompt
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

        # create message array
        messages = []
        if system_prompt is not None:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_prompt})

        # invoke the chat completions endpoint
        chat_completion = self.openai_client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages
        )
        response = chat_completion.choices[0].message.content
        logger.debug("AI Response: %s", response)

        return response
