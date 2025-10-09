import os
import logging
import pandas
import json
from pydantic import BaseModel
from inference_gateway import InferenceGateway
from prompts import prompts

logger = logging.getLogger(__name__)

class FromStringCommand(BaseModel):
    """ Command processor for the From String action."""

    # input parameters
    input_str : str = None

    # configuration


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

        # step 1 - analyze input
        step_1_response = gateway.simple_chat(prompts.STEP_1_ANALYZE, self.input_str)
        logger.info("Step #1 Response == %s", step_1_response)
