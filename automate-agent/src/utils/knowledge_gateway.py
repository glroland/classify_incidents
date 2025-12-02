""" Knowledge Lookup Tool """
import logging
import urllib.request
from utils.settings import settings

logger = logging.getLogger(__name__)

def get_knowledge_artifact(artifact_name: str, fail_on_error=False) -> str:
    """ Retrieves knowledge from the central repository (configurable).  
    
        artifact_name - filename of artifact to retrieve
        fail_on_error - if true, an exception will be raised if the artifact cannot be retrieved
        
        Returns: contents of artifact
    """
    logger.info("get_knowledge_artifact parameters.  Artifact=%s, FailOnError=%s", artifact_name, fail_on_error)

    # validate that required arguments were provided
    if artifact_name is None or len(artifact_name) == 0:
        msg = "ERROR: 'artifact_name' is a required argument and cannot be empty"
        logger.error(msg)
        raise ValueError(msg)

    # download environmental knowledge
    url = settings.KNOWLEDGE_ENVIRONMENT_URL + artifact_name
    logger.info("Downloading Knowledge from: %s", url)
    environmental_knowledge = ""
    try:
        with urllib.request.urlopen(url) as response:
            file_content = response.read()
            environmental_knowledge = file_content.decode('utf-8')
    except urllib.error.URLError as e:
        msg = f"Unable to download Environmental Knowledge due to error!  URL={url}  Error={e}"
        if fail_on_error:
            logger.error(msg)
            raise ValueError(msg)
        else:
            logger.warning(msg)
            return "WARNING: No environmental context is available!  This will negatively impact the quality of any responses provided."

    logger.info("Knowledge Artifact:  %s", environmental_knowledge)
    return environmental_knowledge
