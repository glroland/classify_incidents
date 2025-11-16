""" Create Automation Plan for IT Operation Tool """
import logging

logger = logging.getLogger(__name__)

async def create_plan(user_request: str, research: str) -> str:
    """ (Step 2 of 5)  Create an implementation plan for the provided request from the user and research 
        that has been assembled from the ecosystem.
    
        user_request - (required) user's original request describing automation objective
        research - (required) environmental research that is helpful in generating accurate automation

        Returns: Implementation Plan for the provided automation request
    """
    logger.info("create_plan parameters.  User_Request=%s.  Research=%s", user_request, research)

    # validate that source code was provided
    if user_request is None or len(user_request) == 0:
        msg = "ERROR: 'user_request' is a required argument and cannot be empty"
        logger.error(msg)
        return msg
    if research is None or len(research) == 0:
        msg = "ERROR: 'research' is a required argument and cannot be empty"
        logger.error(msg)
        return msg


    return "PLAN"
