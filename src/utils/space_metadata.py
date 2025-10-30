""" Manage the space metadata file. """
import logging
from gateways.object_storage_gateway import ObjectStorageGateway
from metadata.evaluation_space import EvaluationSpaceMetadata

logger = logging.getLogger(__name__)

def load_metadata(space_id : str) -> EvaluationSpaceMetadata:
    """ Load the metadata for the provided space
    
        space_id - space id
    """
    # validate input
    if space_id is None or len(space_id) == 0:
        msg = "The provided Space ID is empty!"
        logger.error(msg)
        raise ValueError(msg)

    # get space metadata from object storage
    gateway = ObjectStorageGateway()
    path = f"{space_id}/metadata.json"
    metadata_str = gateway.download(path) 

    return EvaluationSpaceMetadata.model_validate_json(metadata_str)

def save_metadata(metadata : EvaluationSpaceMetadata):
    """ Save the provided metadata.
    
        metadata - metadata file
    """
    # validate metadata
    if metadata is None:
        msg = "Metadata provided as input is empty!"
        logger.error(msg)
        raise ValueError(msg)
    if metadata.id is None or len(metadata.id) == 0:
        msg = "Metadata object provided has no ID!"
        logger.error(msg)
        raise ValueError(msg)

    # get space metadata from object storage
    gateway = ObjectStorageGateway()
    path = f"{metadata.id}/metadata.json"

    # gemerate string from obj
    contents = metadata.model_dump_json()

    # create the evaluation space
    gateway = ObjectStorageGateway()
    gateway.upload(path, contents)
