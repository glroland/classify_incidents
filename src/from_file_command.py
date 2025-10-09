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
    COLUMN_AI_SUMMARY : str = "AI Summary"
    COLUMN_AI_CATEGORY : str = "AI Category"
    COLUMN_AI_IS_CONCLUDED : str = "AI Is Concluded"
    COLUMN_AI_STATUS : str = "AI Status"

    # input parameters
    filename_w_path : str = None
    output_filename : str = None

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

        # validate output file
        logger.debug("Output File: %s", self.output_filename)
        if self.output_filename is None or len(self.output_filename) == 0:
            msg = "Output File is a Required Value and Cannot be Empty!"
            logger.error(msg)
            raise ValueError(msg)
        if os.path.exists(self.output_filename):
            msg = f"Output File does not exist!  Path={self.output_filename}"
            logger.error(msg)
            raise ValueError(msg)

        # ensure file is a CSV
        if not abs_filename.lower().endswith(self.EXT_CSV):
            msg = f"Input File is not a CSV file.  Unable to process at this time.  Filename={abs_filename}"
            logger.error(msg)
            raise ValueError(msg)

        # load file
        df = pandas.read_csv(abs_filename, skiprows=1)
        logger.debug("Head: %s", df.head())
        df.info()

        # setup new columns
        new_column_summary = []
        new_column_category = []
        new_column_is_concluded = []
        new_column_status = []

        # process each row
        for index, row in df.iterrows():
            # translate row to a json string
            json_string = json.dumps(row.to_dict())
            logger.debug("Row #%s == %s", index, json_string)

            # process json string
            command = FromStringCommand()
            command.input_str = json_string
            command.go()

            # append outputs to new columns
            new_column_summary.append(command.summary)
            new_column_category.append(command.category)
            new_column_is_concluded.append(command.is_concluded)
            new_column_status.append(command.status)

        # append new columns to data frame
        df[self.COLUMN_AI_SUMMARY] = new_column_summary
        df[self.COLUMN_AI_CATEGORY] = new_column_category
        df[self.COLUMN_AI_IS_CONCLUDED] = new_column_is_concluded
        df[self.COLUMN_AI_STATUS] = new_column_status

        # log new data frame content summary
        logger.debug("Head: %s", df.head())
        df.info()

        # save the file to disk
        logger.info("Saving new content to disk.  Output Filename=%s", self.output_filename)
        df.to_csv(self.output_filename, index=False, encoding='utf-8')
