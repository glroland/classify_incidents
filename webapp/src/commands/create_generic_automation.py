""" Command for create generic automation (i.e. automation playground). """
import logging
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class CreateGenericAutomationCommand(BaseModel):
    """ Command processor for the Create Generic Automation action."""

    # input parameters

    # output responses

    def go(self):
        """ Execute the command. """
        pass
