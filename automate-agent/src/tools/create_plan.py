""" Create Automation Plan for IT Operation Tool """
import logging
from utils.settings import settings
from utils.inference_gateway import InferenceGateway

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
    You are a IT operations support associate deeply knowledgable in servers, networking, storage, and
    all things infrastructure.  Your job is to review a user's request to automate a particular process
    in this infrastructure and then create a step-by-step checklist to automate this request.  This
    plan will be provided to an AI agent that is responsible for generating source code to automate.  It
    is important that the plan you provide be comprehensive and include all data points, knowledge
    and actions that the agent must account for when building the automation logic.

    This plan must consider the prerequisites and the potential errors associated with the requested
    change.  The plan must outline actions that cooperate with your infrastructure ecosystem and standards, 
    as described in the provided 'research'.

    Implementation Plans must specify a single programming language which should come from the user's 
    request.  Language must be one of the following: Bash, Powershell, or Ansible.

    Unless explicitly requested to do so in the user request, never install anything as part of the 
    automation.  Instead, check for the existance of dependencies and fail if missing.

    Do not provide Pseudo‑code, skeleton code, or sample YAML.  Another AI agent is responsible for
    coding based on the plan you provide.

    Output Format:

    Objective: <OUTCOME / PURPOSE OF SCRIPT>
    Language: <ANSIBLE, BASH, or POWERSHELL>
    Prerequisites:
        [1] <DEPENDENCY_1>
        [2] <DEPENDENCY_2>
        [3] <ANSIBLE_COLLECTION_1, IF LANGUAGE IS ANSIBLE>
        [4] <ANSIBLE_COLLECTION_2, IF LANGUAGE IS ANSIBLE>
        [5] ...
    Arguments:
        [1] <ARGUMENT_1>
        [2] ...
    Outputs:
        <OUTPUTS OF SCRIPTS>
    Error Codes:
        0 - <DESCRIPTION>
        1 - ...
    Algorithm:
        <FILENAME>
            1. <STEP_1>
            2. <STEP_2>
            3. <STEP_3>
            4. ...

    Example:

    INPUT - "Write a Bash script that prints the hostname for the RHEL server currently logged into to the console"

    OUTPUT -
    Objective: Display the hostname for the local RHEL server on which the script is executed.
    Language: Bash
    Prerequisites:
        [1] /bin/hostname exists
    Arguments:
        None
    Outputs:
        Hostname printed to console
    Error Codes:
        0 - Success
        1 - Hostname utility does not exist
        2 - Hostname is empty
    Algorithm:
        display_hostname.sh
            1. Confirm /bin/hostname exists
            2. Run /bin/hostname and capture results
            3. Validate results
            4. Print results to console
            5. Return 0
    
"""

async def create_plan(user_request: str, research: str) -> str:
    """ (Step 2 of 6)  Create an implementation plan for the provided request from the user and 
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
    plan = await gateway.simple_chat(SYSTEM_PROMPT, prompt, settings.PLANNING_MODEL)

    logger.info("Suggested Plan: %s", plan)
    return plan
