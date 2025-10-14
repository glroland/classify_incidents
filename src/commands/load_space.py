""" Command for Getting an existing Evaluation Space in web UI. """
import logging
import json
from pathlib import Path
from pydantic import BaseModel
from metadata.evaluation_space import EvaluationSpaceMetadata
from gateways.object_storage_gateway import ObjectStorageGateway

logger = logging.getLogger(__name__)

class LoadSpacesCommand(BaseModel):
    """ Command processor for the Load Evaluation Space action."""

    # input parameters
    space_id : str = None

    # output responses
    metadata : EvaluationSpaceMetadata = None

    def go(self):
        """ Execute the command. """
    
        # validate input parameters
        if self.space_id is None or len(self.space_id) == 0:
            msg = "space_id is a required query parameter but is empty!"
            logger.error(msg)
            raise ValueError(msg)

        # get space metadata from object storage
        gateway = ObjectStorageGateway()
        path = f"{self.space_id}/metadata.json"
        metadata_str = gateway.download(path) 
        self.metadata = EvaluationSpaceMetadata.model_validate_json(metadata_str)

"""
        # create the evaluation space list
        all_files = gateway.list()
        for file in all_files:
            # break the file into parts
            path_object = Path(file)
            parts = path_object.parts

            # find metdata files
            if parts is not None and len(parts) == 2:
                if parts[1] == "metadata.json":
                    # load metadata
                    contents = gateway.download(file)
                    if contents is None or len(contents) == 0:
                        msg = f"Contents of metadata.json is empty!  Filename={file}"
                        logger.error(msg)
                        raise ValueError(msg)

                    # convert contents to strongly typed object
                    metadata = EvaluationSpaceMetadata.model_validate_json(contents)
                    self.spaces.append(metadata)
"""
