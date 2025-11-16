""" Generate Code for a Generated Plan Tool """
import logging
from utils.constants import SUPPORTED_LANGUAGES

logger = logging.getLogger(__name__)

class CreateCoderResponse:
    language : str
    code : str

async def create_code(plan: str) -> CreateCoderResponse:
    """ (Step 4 of 5)  Generates source code to automate the provided automation plan.
    
        plan - (required) implementation plan consisting of all information needed to generate the automation code

        Returns: programming language in which the code is written in and the source code 
    """
    logger.info("create_code parameters.  Plan=%s", plan)

    # validate that required arguments were provided
    if plan is None or len(plan) == 0:
        msg = "ERROR: 'plan' is a required argument and cannot be empty"
        logger.error(msg)
        return msg

    response = CreateCoderResponse()
    response.language = "ansible"
    response.code = "asdf"


    logger.info("create_code response:  Language=%s  SourceCode=%s", response.language, response.code)
    return response
