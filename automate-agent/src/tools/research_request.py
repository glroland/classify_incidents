""" Generate Code for a Generated Plan Tool """
import logging
from utils.knowledge_gateway import get_knowledge_artifact

logger = logging.getLogger(__name__)

KNOWLEDGE_OVERALL = "overall_environment.md"

async def research_request(user_request: str) -> str:
    """ (Step 1 of 6)  Researches a user request in preparation for generating automation.  This includes
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
    return get_knowledge_artifact(KNOWLEDGE_OVERALL)
