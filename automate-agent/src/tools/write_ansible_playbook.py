""" Write an Ansible Playbook to perform the provided implementation plan """
import logging
from utils.inference_gateway import InferenceGateway
from utils.settings import settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
    You are an IT operations programming analyst who is an expert writing Ansible Playbooks.  These playbooks
    are generally managed via Ansible Automation Platform, where inventory, security credentials, etc are
    managed and jobs scheduled.  You will be provided a detailed implementation plan for an automation 
    request in the user prompt.  Write an Ansible playbook that accomplishes the provided plan. 

    Only return the Ansible playbook.  Do not include commentary.

    While translating requirements from the implementation plan to the playbook, always:
    1.) Check for errors every step of the way
    2.) Verify prerequisites for each step
    3.) Log actions
    4.) Include helpful aspects of the implementation plan in the playbook as comments before the respective step

    If additional information is needed in order to implement any steps, fail the development request and ask
    for help.  Never make assumptions.
"""

async def write_ansible_playbook(plan: str) -> str:
    """ (Step 4 of 5)  Generates an Ansible playbook for the automation plan.

        The implementation plan should drive what language is used to write the automation and this tool is used
        when the appropriate output is Ansible.  Implementation Plans should not involve multiple languages.
        Only choose one language per plan.
    
        plan - (required) implementation plan consisting of all information needed to generate the automation code

        Returns: Ansible Playbook YAML 
    """
    logger.info("write_ansible_playbook parameters.  Plan=%s", plan)

    # validate that required arguments were provided
    if plan is None or len(plan) == 0:
        msg = "ERROR: 'plan' is a required argument and cannot be empty"
        logger.error(msg)
        return msg

    gateway = InferenceGateway()

    # write the source code
    source_code = gateway.simple_chat(SYSTEM_PROMPT, plan, settings.CODING_MODEL)
    if source_code is None or len(source_code) == 0:
        msg = f"ERROR: AI responded with an empty string for the Ansible Playbook YAML.  Plan={plan}"
        logger.error(msg)
        return msg
    logger.info("Ansible Playbook: %s", source_code)

    # build response
    logger.info("write_ansible_playbook response:  %s", source_code)
    return source_code
