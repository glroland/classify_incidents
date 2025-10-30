""" Evaluation Space Metadata Type """
from datetime import datetime
from typing import Optional
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
    last_analysis_date : Optional[datetime] = None

    # summary prompt
    summary_prompt : Optional[str] = None

    # summary
    summary : Optional[str] = None
