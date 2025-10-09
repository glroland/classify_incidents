import os
import logging
import pandas
import json
from pydantic import BaseModel
from from_string_command import FromStringCommand
from inference_gateway import InferenceGateway
from prompts import prompts

logger = logging.getLogger(__name__)

class FromFileCommand(BaseModel):
    """ Command processor for the From File action in the CLI."""

    # constants
    MAX_RETRIES : int = 3
    EXT_CSV : str = ".csv"
    UNKNOWN_CATEGORY : str = "Unspecified by AI"
    COLUMN_AI_SUMMARY : str = "AI Summary"
    COLUMN_AI_CATEGORY : str = "AI Category"
    COLUMN_AI_SUBCATEGORY : str = "AI Subcategory"
    COLUMN_AI_IS_CONCLUDED : str = "AI Is Concluded"
    COLUMN_WAS_LABOR_INTENSIVE : str = "AI Was Labor Intensive"
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
        new_column_was_labor_intensive = []
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
            new_column_was_labor_intensive.append(command.was_labor_intensive)
            new_column_status.append(command.status)

        # append new columns to data frame
        df[self.COLUMN_AI_SUMMARY] = new_column_summary
        df[self.COLUMN_AI_SUBCATEGORY] = new_column_category
        df[self.COLUMN_AI_IS_CONCLUDED] = new_column_is_concluded
        df[self.COLUMN_WAS_LABOR_INTENSIVE] = new_column_was_labor_intensive
        df[self.COLUMN_AI_STATUS] = new_column_status

        # create category column
        df = self.generalize_subcategories(df)

        # log new data frame content summary
        logger.debug("Head: %s", df.head())
        df.info()

        # save the file to disk
        logger.info("Saving new content to disk.  Output Filename=%s", self.output_filename)
        df.to_csv(self.output_filename, index=False, encoding='utf-8')

    def generalize_subcategories(self, df):
        """ Takes a dataframe with a subcategory column and uses AI to generalize
            the column list into a shorter list of parent categories.
            
            df - data frame with subcategory column
        """
        # create array for unique subcategories
        subcategories = df[self.COLUMN_AI_SUBCATEGORY].unique()
        subcategories_csv = ','.join(subcategories)
        logger.debug("Subcategories CSV...   '%s'", subcategories_csv)

        # setup inference gateway
        gateway = InferenceGateway()

        category_mappings = None
    
        # convert subcategories into parent categories
        retries = 0
        while retries < self.MAX_RETRIES:
            try:
                categories_json_str = gateway.simple_chat(prompts.ROLLUP_SUBCATEGORIES, subcategories_csv)
                logger.debug("Categories from Subcategories Response == %s", categories_json_str)
                category_mappings = json.loads(categories_json_str)

                break
            except Exception as e:
                logger.warning("An error occurred while trying to create generalized categories list.  Retrying...  Exception=%s", e)
                retries += 1

        # update dataframe with new category column
        new_column_category = []
        for index, row in df.iterrows():
            subcategory = row[self.COLUMN_AI_SUBCATEGORY]
            category = category_mappings[subcategory]
            if category is None:
                logger.warning("Category is unknown - nothing specified for subcategory:  %s", subcategory)
                category = self.UNKNOWN_CATEGORY
            new_column_category.append(category)
        df[self.COLUMN_AI_CATEGORY] = new_column_category

        return df
