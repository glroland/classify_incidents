""" Type for a data file. """
from pydantic import BaseModel

class DataFile(BaseModel):
    """ Metadata format for a data file. """

    filename : str = None
    path : str = None
    parts : list[str] = None
