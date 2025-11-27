""" Generate Code for a Generated Plan Tool """
import logging
import urllib.request
from utils.settings import settings

logger = logging.getLogger(__name__)

async def research_request(user_request: str) -> str:
    """ (Step 1 of 5)  Researches a user request in preparation for generating automation.  This includes
        finding and augumenting the request with related environmental information, such as system types,
        software versions, prior issues, security concerns, etc.
    
        user_request - (required) write up for the user's request for automation

        Returns: Helpful research as it relates to fulling the user's request to generate automation
    """
    logger.info("create_code parameters.  User Request=%s", user_request)

    # validate that required arguments were provided
    if user_request is None or len(user_request) == 0:
        msg = "ERROR: 'user_request' is a required argument and cannot be empty"
        logger.error(msg)
        return msg

    # download environmental knowledge
    logger.info("Downloading Knowledge from: %s", settings.KNOWLEDGE_ENVIRONMENT_URL)
    environmental_knowledge = ""
    try:
        with urllib.request.urlopen(settings.KNOWLEDGE_ENVIRONMENT_URL) as response:
            file_content = response.read()
            environmental_knowledge = file_content.decode('utf-8')
    except urllib.error.URLError as e:
        logger.error("Unable to download Environmental Knowledge due to error!  %s", e)
        return "WARNING: No environmental context is available!  This will negatively impact the quality of any responses provided."

    logger.info("Environmental Knowledge:  %s", environmental_knowledge)
    return environmental_knowledge
