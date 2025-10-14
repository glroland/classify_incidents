""" Command for Creating new Evaluation Space in web UI. """
import logging
import uuid
from pydantic import BaseModel
from metadata.evaluation_space import EvaluationSpaceMetadata
from gateways.object_storage_gateway import ObjectStorageGateway

logger = logging.getLogger(__name__)

class CreateSpaceCommand(BaseModel):
    """ Command processor for the Create Evaluation Space action."""

    # input parameters
    name : str = None
    description : str = None

    # output responses
    id : str = None

    def go(self):
        """ Execute the command. """

        # validate name input
        logger.debug("Input Name: %s", self.name)
        if self.name is None or len(self.name) == 0:
            msg = "Name is a Required Value and Cannot be Empty!"
            logger.error(msg)
            raise ValueError(msg)

        # generate id
        my_uuid_object = uuid.uuid4()
        self.id = str(my_uuid_object)

        # setup evaluation metadata file
        metadata = EvaluationSpaceMetadata()
        metadata.id = self.id
        metadata.name = self.name
        metadata.description = self.description
        contents = metadata.model_dump_json()

        # build metadata path
        path = f"{self.id}/metadata.json"

        # create the evaluation space
        gateway = ObjectStorageGateway()
        gateway.upload(path, contents)
