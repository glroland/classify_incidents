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

    # configuration

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
        step_2_response = gateway.json_chat(settings.OPENAI_MODEL, prompts.STEP_2_ANALYZE, step_1_response)
        logger.info("Step #2 Response == %s", step_2_response)
        analysis = step_2_response
        self.asset_name = analysis["asset_name"]
        self.category = analysis["category"]
        self.is_manual = analysis["is_manual"]
        self.is_outage = analysis["is_outage"]
        self.status = analysis["status"]

        if "date_reported" in analysis:
            date_reported_str = analysis["date_reported"]
            self.date_reported = self.str_to_datetime(date_reported_str)
            logger.info("Date Reported.  Str=%s. Obj=%s", date_reported_str, self.date_reported)

        if "date_resolved" in analysis:
            date_resolved_str = analysis["date_resolved"]
            self.date_resolved = self.str_to_datetime(date_resolved_str)
            logger.info("Date Resolved.  Str=%s. Obj=%s", date_resolved_str, self.date_resolved)

    def str_to_datetime(self, datetime_s: str) -> datetime:
        """ Converts a date/time in string format to a storngly typed date time object.
        
            datetime_s - datetime as string
            
            Returns: datetime
        """
        # validate arguments
        if datetime_s is None or len(datetime_s) == 0:
            logger.warning("datetime_s is a required argument but is empty!  Returning datetime as None")
            return None

        # format #1
        format : str = "%Y/%m/%d %H:%M:%S"
        try:
            return datetime.strptime(datetime_s, format)
        except ValueError as e:
            logger.debug("datetime_s did not match the expected format.  S=%. F=%", datetime_s, format)

        # format #2
        format : str = "%Y-%m-%d %H:%M:%S"
        try:
            return datetime.strptime(datetime_s, format)
        except ValueError as e:
            logger.debug("datetime_s did not match the expected format.  S=%. F=%", datetime_s, format)

        # unable to format string
        msg = f"Unable to convert string to datetime!  S={datetime_s}"
        logger.error(msg)
        raise ValueError(msg)
