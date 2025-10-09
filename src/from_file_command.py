import os
import logging
import pandas
import json
from pydantic import BaseModel
from from_string_command import FromStringCommand

logger = logging.getLogger(__name__)

class FromFileCommand(BaseModel):
    """ Command processor for the From File action in the CLI."""

    # constants
    EXT_CSV : str = ".csv"

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
        abs_filename = os.path.abspath(self.filename_w_path)
        logger.info("Input File (Absolute): %s", abs_filename)

        # ensure file is a CSV
        if not abs_filename.lower().endswith(self.EXT_CSV):
            msg = f"Input File is not a CSV file.  Unable to process at this time.  Filename={abs_filename}"
            logger.error(msg)
            raise ValueError(msg)

        # load file
        df = pandas.read_csv(abs_filename, skiprows=1)
        logger.debug("Head: %s", df.head())
        df.info()

        # process each row
        for index, row in df.iterrows():
            # translate row to a json string
            json_string = json.dumps(row.to_dict())
            logger.debug("Row #%s == %s", index, json_string)

            # process json string
            command = FromStringCommand()
            command.input_str = json_string
            command.go()
