""" Write Powershell Script to implement the provided implementation plan """
import logging
from utils.inference_gateway import InferenceGateway
from utils.settings import settings
from utils.knowledge_gateway import get_knowledge_artifact

logger = logging.getLogger(__name__)

KNOWLEDGE_POWERSHELL_BEST_PRACTICES = "powershell_best_practices.md"

SYSTEM_PROMPT = """
    You are an IT operations programming analyst who is an expert writing PowerShell scripts to
    automate tasks around the Windows operating system.  These scripts will be designed to run on a single 
    system as an Administrative user.  Since these scripts are used by individual admins, runtime 
    configuration like endpoints and service names must be provided as command line arguments and security 
    credentials provided as environment variables when not inherited from the operating system context of 
    the user running the script.  You will be provided a detailed implementation plan for an automation 
    request in the user prompt.  Write a PowerShell script that accomplishes the provided plan. 

    Only return the PowerShell script.  Do not include commentary.

    While translating requirements from the implementation plan to the script, always:
    1.) Check for errors every step of the way
    2.) Verify prerequisites for each step
    3.) Log actions to the console
    4.) Include helpful aspects of the implementation plan in the playbook as comments before the respective step

    If additional information is needed in order to implement any steps, fail the development request and ask
    for help.  Never make assumptions.

    All scripts produced must align with following standards and practices:
"""

async def write_powershell_script(plan: str) -> str:
    """ (Step 5c of 6)  Generates a PowerShell Script for the automation plan.

        The implementation plan should drive what language is used to write the automation and this tool is used
        when the appropriate output is a PowerShell Script.  Implementation Plans should not involve multiple 
        languages.  Only choose one language per plan.
    
        plan - (required) implementation plan consisting of all information needed to generate the automation code

        Returns: Bash Shell Script 
    """
    logger.info("write_powershell_script parameters.  Plan=%s", plan)

    # validate that required arguments were provided
    if plan is None or len(plan) == 0:
        msg = "ERROR: 'plan' is a required argument and cannot be empty"
        logger.error(msg)
        return msg

    # build system prompt
    best_practices = get_knowledge_artifact(KNOWLEDGE_POWERSHELL_BEST_PRACTICES)
    system_prompt = SYSTEM_PROMPT + best_practices
    logger.debug("Final System Prompt: %s", system_prompt)

    gateway = InferenceGateway()

    # write the source code
    source_code = gateway.simple_chat(system_prompt, plan, settings.CODING_MODEL)
    if source_code is None or len(source_code) == 0:
        msg = f"ERROR: AI responded with an empty string for the PowerShell script.  Plan={plan}"
        logger.error(msg)
        return msg
    logger.info("PowerShell Script: %s", source_code)

    # build response
    logger.info("write_powershell_script response:  %s", source_code)
    return source_code
