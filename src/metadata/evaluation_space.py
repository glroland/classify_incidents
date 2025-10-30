""" Evaluation Space Metadata Type """
from datetime import datetime
from pydantic import BaseModel

class EvaluationSpaceMetadata(BaseModel):
    """ Data Type for the Evaluation Space Metadata File """

    # evaluation space id
    id : str = ""

    # name of evaluation space
    name : str = ""

    # description of evaluation space
    description : str = ""

    # last incident analysis date
    last_analysis_date : datetime = None

    # summary prompt
    summary_prompt : str = ""

    # summary
    summary : str = ""
