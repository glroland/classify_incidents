""" AI Prompts for analyzing instancts. """
import os
import logging
import requests
from utils.settings import settings

logger = logging.getLogger(__name__)

# pylint: disable=too-few-public-methods
class Prompts:
    """ List of prompts used througout application. """

    # filenames
    STEP_1_SUMMARIZE_FILENAME : str = "step_1_summarize.txt"
    STEP_2_ANALYZE_FILENAME : str = "step_2_analyze.txt"
    ROLLUP_SUBCATEGORIES_FILENAME : str = "rollup_subcategories.txt"

    # prompts
    # pylint: disable=invalid-name
    STEP_1_SUMMARIZE : str = None
    STEP_2_ANALYZE : str = None
    ROLLUP_SUBCATEGORIES : str = None

    # other constants
    HTTP : str = "http"
    ENCODING : str = "utf-8"

    def __init__(self):
        """ Default Constructor """
        self.STEP_1_SUMMARIZE = self.load_prompt(self.STEP_1_SUMMARIZE_FILENAME)
        self.STEP_2_ANALYZE = self.load_prompt(self.STEP_2_ANALYZE_FILENAME)
        self.ROLLUP_SUBCATEGORIES = self.load_prompt(self.ROLLUP_SUBCATEGORIES_FILENAME)

    def load_prompt(self, filename : str) -> str:
        """ Loads the specified prompt from disk or a remote server. 
        
            filename - name of the file to source
        """
        # validate parameters
        if filename is None or len(filename) == 0:
            msg = "Filename parameter is required for loading prompts but is empty!"
            logger.error(msg)
            raise ValueError(msg)

        # get and analyze prompt directory
        prompts_location = settings.PROMPTS_LOCATION
        if prompts_location is None or len(prompts_location) == 0:
            msg = "Prompts Location is a required setting but is empty!"
            logger.error(msg)
            raise ValueError(msg)

        prompt_contents = None

        # load from network
        if str(prompts_location).lower().startswith(self.HTTP):
            logger.debug("Loading Prompt from URL: %s", prompts_location)

            # build URL
            url = str(prompts_location)
            if url[-1] != "/":
                url += "/"
            url += filename
            logger.debug("Prompt File URL: %s", url)

            # request file
            http_response = requests.get(url)
            if http_response.status_code != 200:
                msg = f"Unable to retrieve prompt from URL.  Code={url}"
                logger.error(msg)
                raise ValueError(msg)

            prompt_contents = http_response.text

        # load from disk
        else:
            logger.debug("Loading Prompt from Disk: %s", filename)

            # build filename
            path = os.path.join(prompts_location, filename)
            abs_path = os.path.abspath(path)
            logger.info("Absolute Path to File: %s", abs_path)

            # load file
            with open(abs_path, "r", encoding=self.ENCODING) as file:
                prompt_contents = file.read()

        logger.debug("Prompt for %s: %s", filename, prompt_contents)
        return prompt_contents

prompts = Prompts()
