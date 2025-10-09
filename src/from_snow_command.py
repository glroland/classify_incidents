import logging
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class FromServiceNowCommand(BaseModel):
    """ Command processor for the From SNOW action in the CLI."""

    def go():
        """ Execute the command. """
        pass
