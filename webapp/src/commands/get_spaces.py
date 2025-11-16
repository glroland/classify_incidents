""" Command for Getting a list of existing Evaluation Spaces in web UI. """
import logging
from pathlib import Path
from pydantic import BaseModel
from metadata.evaluation_space import EvaluationSpaceMetadata
from gateways.object_storage_gateway import ObjectStorageGateway

logger = logging.getLogger(__name__)

class GetSpacesCommand(BaseModel):
    """ Command processor for the Get Evaluation Spaces action."""

    # output responses
    spaces : list[EvaluationSpaceMetadata] = []

    def go(self):
        """ Execute the command. """

        # create the evaluation space list
        gateway = ObjectStorageGateway()
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
