""" Generate Code for a Generated Plan Tool """
import logging
from utils.constants import SUPPORTED_LANGUAGES
from utils.inference_gateway import InferenceGateway
from utils.settings import settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT_GET_LANGUAGE = """
    The implementation plan for an automation request will be provided in the user prompt.  Review this
    and identify what programming language it is suggesting we use to develop the resulting source code.
    The response must be a single word and that word should be the name of the programming language.

    In the event that you are unable to identify any programming language from the input, response with n/a.

    Example 1 Word Responses:
    java
    bash
    ansible
    n/a
"""

SYSTEM_PROMT_WRITE_SOURCE_CODE = """
    You are an IT operations engineer who specializes in automating technical activities.  You are 
    provided a detailed implementation plan in the user prompt and are expected to write source code
    to automate each step of the implementation plan.  

    Always check for errors.

    If additional information is needed in order to implement any steps, always ask for help and never
    assume.

    The automation must be developed in the following programming language:
"""

class CreateCoderResponse:
    language : str
    source_code : str

async def get_source_code(plan: str) -> CreateCoderResponse:
    """ (Step 4 of 5)  Generates source code to automate the provided automation plan.
    
        plan - (required) implementation plan consisting of all information needed to generate the automation code

        Returns: programming language in which the code is written in and the source code 
    """
    logger.info("get_source_code parameters.  Plan=%s", plan)

    # validate that required arguments were provided
    if plan is None or len(plan) == 0:
        msg = "ERROR: 'plan' is a required argument and cannot be empty"
        logger.error(msg)
        return msg

    gateway = InferenceGateway()

    # determine language to use
    language = gateway.simple_chat(SYSTEM_PROMPT_GET_LANGUAGE, plan, settings.CODING_MODEL)
    if language is None or len(language) == 0:
        msg = f"ERROR: AI responded with an empty string for programming language.  Plan={plan}"
        logger.error(msg)
        return msg
    logger.debug("Raw Language Response: %s", language)
    language = language.strip().lower()
    logger.info("Suggested Language:  %s", language)
    if language == "n/a":
        msg = f"ERROR: AI was unable to determine what programming language to use for automation."
        logger.error(msg)
        return msg
    if not language in SUPPORTED_LANGUAGES:
        msg = f"ERROR: The suggested programming language to use based on the Implementation Plan is not supported.  Language={language}"
        logger.error(msg)
        return msg

    # write the source code
    prompt = SYSTEM_PROMT_WRITE_SOURCE_CODE + language
    source_code = gateway.simple_chat(prompt, plan, settings.CODING_MODEL)
    if source_code is None or len(source_code) == 0:
        msg = f"ERROR: AI responded with an empty string for source code.  Language={language} Plan={plan}"
        logger.error(msg)
        return msg
    logger.info("Source Code: %s", source_code)

    # build response
    response = CreateCoderResponse()
    response.language = language
    response.source_code = source_code
    logger.info("create_code response:  Language=%s  SourceCode=%s", response.language, response.code)
    return response
