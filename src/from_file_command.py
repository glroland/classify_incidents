import os
import logging
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class FromFileCommand(BaseModel):
    """ Command processor for the From File action in the CLI."""

    # input parameters
    filename_w_path : str = None

    # configuration


    def go(self):
        """ Execute the command. """
        # validate input file
        logger.debug("Input File: %s", self.filename_w_path)
        if self.filename_w_path is None or len(self.filename_w_path) == 0:
            msg = "Input File is a Required Value and Cannot be Empty!"
            logger.error(msg)
            raise ValueError(msg)
        if not os.path.exists(self.filename_w_path):
            msg = f"Input File does not exist!  Path={self.filename_w_path}"
            logger.error(msg)
            raise ValueError(msg)
        if not os.path.exists(self.filename_w_path):
            msg = f"Input File does not exist!  Path={self.filename_w_path}"
            logger.error(msg)
            raise ValueError(msg)
        if not os.path.isfile(self.filename_w_path):
            msg = f"Input File exists but is not a file!  Path={self.filename_w_path}"
            logger.error(msg)
            raise ValueError(msg)
        abs_path = os.path.abspath(self.filename_w_path)
        logger.info("Input File (Absolute): %s", abs_path)

        # process file


        pass
