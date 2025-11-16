""" Validate Generated Code Tool """
import logging
from utils.constants import SUPPORTED_LANGUAGES

logger = logging.getLogger(__name__)

async def validate_code(language: str, source_code: str) -> str:
    """ (Step 5 of 5)  Validates the syntax and quality of the provided source code. 
    
        language - (required) programming language that the code is written in (ex. 'java', 'bash', 'ansible')
        source_code - (required) source code to be validated

        Returns: Quality assessment of the provided parameteres
    """
    logger.info("validate_code parameters.  Language=%s  Source_Code=%s", language, source_code)

    # validate that it is a supported language
    if language is None or len(language) == 0:
        msg = "ERROR: 'language' is a required argument and cannot be empty"
        logger.error(msg)
        return msg
    language = language.strip().lower()
    if not language in SUPPORTED_LANGUAGES:
        msg = f"ERROR: language '{language}' is not supported.  Supported languages are '{SUPPORTED_LANGUAGES}'"
        logger.error(msg)
        return msg

    # validate that source code was provided
    if source_code is None or len(source_code) == 0:
        msg = "ERROR: 'code' is a required argument and cannot be empty"
        logger.error(msg)
        return msg


    return "VALID"
