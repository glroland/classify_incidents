""" Revise Automation Plan based on feedback from Judge """
import logging
from utils.settings import settings
from utils.inference_gateway import InferenceGateway

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
    You are an IT analyst whose job is to revise implementation plans that are used by AI agents
    to create automation scripts.  You will be provided feedback on an implementation and must
    revise the plan to accomodate the feedback.
    
    The modified plan should be in the same format as the provided plan that you modified.

    You must not generally enhance the plan in any way.  Only modify based on specific feedback
    provided an input.

    In the event you disagree with a change, raise an error.
"""

async def revise_plan(feedback: str, plan: str) -> str:
    """ (Step 4 of 6)  Revises a previously created implmentation plan to accomodate improvement suggestions
        and errors.
    
        feedback - (required) list of issues to remediate and improvements to make
        plan - (required) implementation plan to modify

        Returns: Revised implementation plan
    """
    logger.info("revise_plan parameters.  Feedback=%s.  Plan=%s", feedback, plan)

    # validate that source code was provided
    if feedback is None or len(feedback) == 0:
        msg = "ERROR: 'feedback' is a required argument and cannot be empty"
        logger.error(msg)
        return msg
    if plan is None or len(plan) == 0:
        msg = "ERROR: 'plan' is a required argument and cannot be empty"
        logger.error(msg)
        return msg

    # build user prompt
    prompt = f"""Feedback:
        {feedback}

        Implementation Plan:
        {plan}"""

    # execute inference
    gateway = InferenceGateway()
    plan = await gateway.simple_chat(SYSTEM_PROMPT, prompt, settings.PLANNING_MODEL)

    logger.info("Updated Plan: %s", plan)
    return plan
