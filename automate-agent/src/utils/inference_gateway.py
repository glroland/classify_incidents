""" Service Gateway for the Inferencing API. """
import logging
import json
from openai import AsyncOpenAI
from utils.settings import settings

logger = logging.getLogger(__name__)

# pylint: disable=too-few-public-methods
class InferenceGateway():
    """ OpenAI Service Gateway """

    # openai client
    openai_client : AsyncOpenAI = None

    def __init__(self):
        """ Default Constructor """
        self.openai_client = AsyncOpenAI(base_url=settings.OPENAI_BASE_URL,
                                         api_key=settings.OPENAI_API_KEY)

    async def simple_chat(self, system_prompt, user_prompt, model):
        """ Executes a simple chat based on the provided prompts.

            system_prompt - system prompt
            user_prompt - user prompt
        """
        # validate required fields
        if user_prompt is None or len(user_prompt) == 0:
            msg = "User Prompt is a required field and cannot be empty!"
            logger.error(msg)
            raise ValueError(msg)
        if model is None or len(model) == 0:
            msg = "Model is a required field and cannot be empty!"
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
        chat_completion = await self.openai_client.chat.completions.create(
            model=model,
            messages=messages
        )
        response = chat_completion.choices[0].message.content
        logger.debug("AI Response: %s", response)

        return response


    async def json_chat(self, system_prompt, user_prompt, model):
        """ Executes a simple chat based on the provided prompts that responds in JSON

            system_prompt - system prompt
            user_prompt - user prompt
            model - model to use
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
        response = await self.openai_client.responses.create(
            model=model,
            instructions=system_prompt,
            input=user_prompt,
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
        ai_response = ai_response.strip().removeprefix("```")
        ai_response = ai_response.strip().removeprefix("final")
        ai_response = ai_response.strip().removeprefix("json")
        ai_response = ai_response.strip().removesuffix("```")
        json_obj = json.loads(ai_response)

        return json_obj
