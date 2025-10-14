""" Evaluation Space Metadata Type """
from pydantic import BaseModel

class EvaluationSpaceMetadata(BaseModel):
    """ Data Type for the Evaluation Space Metadata File """

    # evaluation space id
    id : str = ""

    # name of evaluation space
    name : str = ""

    # description of evaluation space
    description : str = ""
