""" Judge Generated Plan Tool """
import logging

logger = logging.getLogger(__name__)

async def judge_plan(user_request: str, research: str, nominated_plan: str) -> str:
    """ (Step 3 of 5)  Review the provided implementation plan for an automation generation request for
        accuracy and quality.  The result will be suggestions and criticism, if any, that must be 
        incorporated into the implementation plan.  If the suggested plan is modified based on the
        feedback, it must be re-judged by reinvoking this tool.
    
        user_request - (required) write up for the user's request for automation
        research - (required) helpful research as it relates to implementing the user's automation request
        suggested_plan - nominated implementation plan for the request

        Returns: Quality assessment of the provided parameteres
    """
    logger.info("judge_plan parameters.  User_Request=%s  Research=%s. Nominated_Plan=%s",\
                user_request, research, nominated_plan)

    # validate that all required parameters were provided
    if user_request is None or len(user_request) == 0:
        msg = "ERROR: 'user_request' is a required argument and cannot be empty"
        logger.error(msg)
        return msg
    if research is None or len(research) == 0:
        msg = "ERROR: 'research' is a required argument and cannot be empty"
        logger.error(msg)
        return msg
    if nominated_plan is None or len(nominated_plan) == 0:
        msg = "ERROR: 'nominated_plan' is a required argument and cannot be empty"
        logger.error(msg)
        return msg


    return "VALID"
