""" CLI Command for Analyzing Incidents directly from Service Now. """
import logging
from pydantic import BaseModel
from gateways.snow_gateway import ServiceNowGateway

logger = logging.getLogger(__name__)

class FromServiceNowCommand(BaseModel):
    """ Command processor for the From SNOW action in the CLI."""

    def go(self):
        """ Execute the command. """

        # build parameters list
        parameters = []

        # query service now
        gateway = ServiceNowGateway()
        results = gateway.query_snow(parameters)
