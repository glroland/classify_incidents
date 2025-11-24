""" Command for Analyzing Instances via raw text. """
import logging
import json
from datetime import datetime
from pydantic import BaseModel
from gateways.inference_gateway import InferenceGateway
from utils.get_prompt import prompts
from utils.settings import settings

logger = logging.getLogger(__name__)

class FromStringCommand(BaseModel):
    """ Command processor for the From String action."""

    # constants
    DATETIME_FORMAT : str = "%Y/%m/%d %H:%M:%S"

    # configuration
    MAX_RETRIES : int = 3

    # input parameters
    input_str : str = None

    # output responses
    summary : str = None
    asset_name : str = None
    category : str = None
    is_manual : bool = None
    is_outage : bool = None
    status : str = None
    date_reported : datetime = None
    date_resolved : datetime = None

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
        step_1_response = gateway.simple_chat(settings.OPENAI_MODEL, prompts.STEP_1_SUMMARIZE, self.input_str)
        logger.info("Step #1 Response == %s", step_1_response)
        self.summary = step_1_response

        # step 2 - Analyze summary
        retries = 0
        while retries < self.MAX_RETRIES:
            try:
                step_2_response = gateway.simple_chat(settings.OPENAI_MODEL, prompts.STEP_2_ANALYZE, step_1_response)
                logger.info("Step #2 Response == %s", step_2_response)
                analysis = json.loads(step_2_response)
                self.asset_name = analysis["asset_name"]
                self.category = analysis["category"]
                self.is_manual = analysis["is_manual"]
                self.is_outage = analysis["is_outage"]
                self.status = analysis["status"]

                if "date_reported" in analysis:
                    date_reported_str = analysis["date_reported"]
                    if date_reported_str is not None and len(date_reported_str) > 0:
                        self.date_reported = datetime.strptime(date_reported_str, self.DATETIME_FORMAT)                
                    logger.info("Date Reported.  Str=%s. Obj=%s", date_reported_str, self.date_reported)

                if "date_resolved" in analysis:
                    date_resolved_str = analysis["date_resolved"]
                    if date_resolved_str is not None and len(date_resolved_str) > 0:
                        self.date_resolved = datetime.strptime(date_resolved_str, self.DATETIME_FORMAT)  
                    logger.info("Date Resolved.  Str=%s. Obj=%s", date_resolved_str, self.date_resolved)

                break
            except Exception as e:  # pylint: disable=broad-exception-caught
                logger.warning("Retrying after error raised while trying to analyze summary.  E=%s", e) # pylint: disable=line-too-long
                retries += 1
