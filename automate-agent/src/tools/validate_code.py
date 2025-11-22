""" Validate Generated Code Tool """
import os
import logging
import uuid
import subprocess
from utils.constants import SUPPORTED_LANGUAGES, LANGUAGE_ANSIBLE, LANGUAGE_BASH, LANGUAGE_POWERSHELL
from utils.settings import settings

logger = logging.getLogger(__name__)

def validate_ansible(source_file):
    """ Validates the provided Ansible playbook code using Ansible Lint.
    
        source_file - Ansible Playbook
    
        Returns: validation results
    """
    logger.info("Validating Ansible Playbook: Filename=%s", source_file)

    # run ansible lint
    command = ["ansible-lint", "-f", "pep8", "--skip-list", "yaml[trailing-spaces],yaml[empty-lines]", "--nocolor", "--project-dir", "/tmp", source_file]
    validation_response = None
    try:
        logger.info("Running ansible-lint:  Command=%s", command)
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        logger.info("Ansible Lint completed successfully.  Stdout=%s. Stderr=%s", result.stdout, result.stderr)
        validation_response = result.stderr
    except subprocess.CalledProcessError as e:
        logger.warning("Ansible Lint failed with errors.  Stderr=%s  Stdout=%s", e.stderr, e.stdout)
        validation_response = e.stdout
    except FileNotFoundError:
        msg = "ERROR: Ansible-lint command not found.  Ensure its installed and in PATH."
        logger.fatal(msg)
        validation_response = msg

    # cleanse response
    validation_response = str(validation_response).replace(source_file + ":", "")
    validation_response = validation_response.replace("/private", "")
    return validation_response


def validate_bash(source_file):
    """ Validates the provided Bash Script.
    
        source_file - Bash Script
    
        Returns: validation results
    """
    logger.info("Validating Bash Schell Script: Filename=%s", source_file)

    # run shellcheck
    command = ["shellcheck", source_file]
    try:
        logger.info("Running shellcheck:  Command=%s", command)
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False  # ShellCheck returns non-zero for warnings/errors
        )
        if result.returncode == 0:
            logger.info("Shellcheck completed successfully.  Result=%s", result.stdout)
            return result.stdout
        else:
            logger.error("Shellcheck reponded with an error.  Error=%s", result.stdout)
            return "ERROR: " + result.stdout
    except FileNotFoundError:
        msg = "ERROR: ShellCheck not found. Please install it and add to PATH."
        logger.error(msg)
        return msg


def validate_powershell(source_file):
    """ Validates the provided Powershell Script.
    
        source_file - Powershell Script
    
        Returns: validation results
    """
    logger.info("Validating PowerShell Script: Filename=%s", source_file)

    # run shellcheck
    command = ["pwsh", "-Command", f"Invoke-ScriptAnalyzer -Path '{source_file}' | ConvertTo-Json"]
    try:
        logger.info("Running pwsh:  Command=%s", command)
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )

        # PSScriptAnalyzer returns JSON output if successful.
        # If there are no errors, the JSON list might be empty.
        if "[]" in result.stdout.strip() or not result.stdout.strip():
            msg = f"Syntax check passed.  No errors detected in powershell script."
            logger.info(msg)
            return msg
        else:
            msg = f"ERROR: Syntax errors found in powershell script!  Errors={result.stdout}"
            logger.error(msg)
            return msg

    except subprocess.CalledProcessError as e:
        logger.error("Powershell failed with errors.  Result=%s", e.stderr)
        return "ERROR: " + e.stderr
    except FileNotFoundError:
        msg = "ERROR: Powershell not found. Please install it and add to PATH."
        logger.error(msg)
        return msg


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

    # create filename (dependencies actually require this to be accurate)
    filename = str(uuid.uuid4())
    if language == LANGUAGE_ANSIBLE:
        filename += ".yaml"
    elif language == LANGUAGE_BASH:
        filename += ".sh"
    elif language == LANGUAGE_POWERSHELL:
        filename += ".ps1"
    logger.debug("Temp Filename = %s", filename)

    # save source to a temp file on disk
    temp_file_path = os.path.join(settings.WORK_DIR, filename)
    logger.info("Writing source code to a temp file.  Name=%s", temp_file_path)
    with open(temp_file_path, "w") as file:
        file.write(source_code)
    logger.info("Source code written to disk.  Moving to validation.")

    # validate source code
    result = None
    if language == LANGUAGE_ANSIBLE:
        result = validate_ansible(temp_file_path)
    elif language == LANGUAGE_BASH:
        result = validate_bash(temp_file_path)
    elif language == LANGUAGE_POWERSHELL:
        result = validate_powershell(temp_file_path)

    # delete the temp file
    #os.remove(temp_file_path)

    # return result
    if result is None:
        result = "Unable to validate source code.  Assuming to be fine."
    logger.info("Validation Result: %s", result)
    return result
