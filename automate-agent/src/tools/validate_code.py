""" Validate Generated Code Tool """
import os
import logging
import uuid
import subprocess
from utils.constants import SUPPORTED_LANGUAGES, LANGUAGE_ANSIBLE
from utils.settings import settings

logger = logging.getLogger(__name__)

def validate_ansible(playbook_code):
    """ Validates the provided Ansible playbook code using Ansible Lint.
    
        playbook_code - Ansible Playbook
    
        Returns: validation results
    """
    # save playbook to a temp file on disk
    filename = uuid.uuid4() + ".yaml"
    temp_file_path = os.path.join(settings.WORK_DIR, filename)

    # Create and write to the temporary file
    with open(temp_file_path, "w") as file:
        file.write(playbook_code)

    # run ansible lint
    command = ["ansible-lint", temp_file_path]
    response = None
    try:
        logger.info("Running ansible-lint:  Command=%s", command)
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        logger.info("Ansible Lint completed successfully.  Result=%s", result.stdout)
        response = result.stdout
    except subprocess.CalledProcessError as e:
        logger.error("Ansible Lint failed with errors.  Result=%s", e.stderr)
        response = e.stderr
    except FileNotFoundError:
        msg = "ERROR: Ansible-lint command not found.  Ensure its installed and in PATH."
        logger.fatal(msg)
        response = msg

    # delete the temp file
    os.remove(temp_file_path)

    return response


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

    # validate ansible
    if language == LANGUAGE_ANSIBLE:
        return validate_ansible(source_code)

    return "Unable to validate source code.  Assuming to be fine."
