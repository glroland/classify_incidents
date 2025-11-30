""" Command for create automation for a given incident. """
import logging
from pydantic import BaseModel
from metadata.evaluation_space import EvaluationSpaceMetadata

logger = logging.getLogger(__name__)

class CreateAutomationFromIncidentCommand(BaseModel):
    """ Command processor for the Create Automation from Incident action."""

    # input parameters
    space_metadata : EvaluationSpaceMetadata = None
    incident_analysis : list[str] = None
    raw_incident_data : str = None

    # output responses
    id : str = None

    def go(self):
        """ Execute the command. """
        pass
