""" Create Automation Plan for IT Operation Tool """
import logging
from utils.settings import settings
from utils.inference_gateway import InferenceGateway

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
    You are a IT operations support associate deeply knowledgable in servers, networking, storage, and
    all things infrastructure.  Your job is to review a user's request to automate a particular process
    in this infrastructure and then create a detailed, step-by-step plan to automate this request.  This
    plan will be provided to an AI agent that is responsible for generating source code to automate.  It
    is important that the plan you provide be comprehensive and include all data points, knowledge
    and actions that the agent must account for when building the automation logic.

    This plan must consider the prerequisites and the potential errors associated with the requested
    change.  The plan must outline actions that cooperate with your infrastructure ecosystem and standards, 
    as described in the provided 'research'.

    Implementation Plans must specific a single programming language which should come from the user's 
    request.  If a language was not provided, assume that an Ansible Playbook is to be developed.

    Implementation Plan complexity and detail should be commensurate with the user's request.  Avoid 
    excessive planning for simple requests.
"""

async def create_plan(user_request: str, research: str) -> str:
    """ (Step 2 of 5)  Create an implementation plan for the provided request from the user and 
        research that has been assembled from the ecosystem.
    
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

    # build user prompt
    prompt = f"""{user_request}

        Context:
        {research}"""

    # execute inference
    gateway = InferenceGateway()
    plan = gateway.simple_chat(SYSTEM_PROMPT, prompt, settings.PLANNING_MODEL)

    logger.info("Suggested Plan: %s", plan)
    return plan
