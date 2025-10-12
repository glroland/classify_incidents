""" Command for Analyzing Instances via raw text. """
import logging
import json
from pydantic import BaseModel
from inference_gateway import InferenceGateway
from prompts import prompts

logger = logging.getLogger(__name__)

class FromStringCommand(BaseModel):
    """ Command processor for the From String action."""

    # configuration
    MAX_RETRIES : int = 3

    # input parameters
    input_str : str = None

    # output responses
    summary : str = None
    category : str = None
    is_concluded : bool = None
    was_labor_intensive : bool = None
    status : str = None

    def go(self):
        """ Execute the command. """

        # validate input file
        logger.debug("Input String: %s", self.input_str)
        if self.input_str is None or len(self.input_str) == 0:
            msg = "Input String is a Required Value and Cannot be Empty!"
            logger.error(msg)
            raise ValueError(msg)

        # setup inferencing gateway
        gateway = InferenceGateway()

        # step 1 - Summarize input
        step_1_response = gateway.simple_chat(prompts.STEP_1_SUMMARIZE, self.input_str)
        logger.info("Step #1 Response == %s", step_1_response)
        self.summary = step_1_response

        # step 2 - Analyze summary
        retries = 0
        while retries < self.MAX_RETRIES:
            try:
                step_2_response = gateway.simple_chat(prompts.STEP_2_ANALYZE, step_1_response)
                logger.info("Step #2 Response == %s", step_2_response)
                analysis = json.loads(step_2_response)
                self.category = analysis["category"]
                self.is_concluded = analysis["is_concluded"]
                self.was_labor_intensive = analysis["was_labor_intensive"]
                self.status = analysis["status"]

                break
            except Exception as e:  # pylint: disable=broad-exception-caught
                logger.warning("Retrying after error raised while trying to analyze summary.  E=%s", e) # pylint: disable=line-too-long
                retries += 1
