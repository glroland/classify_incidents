""" CLI Command for Analyzing Instances from a single file. """
import os
import logging
import json
import pandas
from pydantic import BaseModel
from commands.from_string import FromStringCommand
from gateways.inference_gateway import InferenceGateway
from utils.get_prompt import prompts
from utils.settings import settings

logger = logging.getLogger(__name__)

class FromFileCommand(BaseModel):
    """ Command processor for the From File action in the CLI."""

    # constants
    MAX_RETRIES : int = 5
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

   # pylint: disable=too-many-statements
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
            msg = f"Input File is not a CSV file and cannot process. Filename={abs_filename}"
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
        logger.info("Generalizing Subcategories")

        # handle condition where there are no subcategories
        subcategories = df[self.COLUMN_AI_SUBCATEGORY].unique()
        if subcategories is None or len(subcategories) == 0:
            logger.error("No subcategories exist in data frame suggesting invalid AI output.")
            return df

        # create array for unique subcategories
        subcategories_csv = ""
        for subcategory in subcategories:
            if subcategory is not None and len(subcategory) > 0:
                if len(subcategories_csv) > 0:
                    subcategories_csv += ","
                subcategories_csv += subcategory
        logger.debug("Subcategories CSV...   '%s'", subcategories_csv)

        # setup inference gateway
        gateway = InferenceGateway()

        category_mappings = None

        # convert subcategories into parent categories
        retries = 0
        while retries < self.MAX_RETRIES:
            try:
                categories_json_str = gateway.simple_chat(settings.OPENAI_MODEL,
                                                          prompts.ROLLUP_SUBCATEGORIES,
                                                          subcategories_csv)
                logger.debug("Categories from Subcategories Response == %s", categories_json_str)
                category_mappings = json.loads(categories_json_str)

                if category_mappings is not None:
                    break
            except Exception as e:  # pylint: disable=broad-exception-caught
                logger.warning("An error occurred while trying to create generalized categories list.  Retrying...  Exception=%s", e)   # pylint: disable=line-too-long
                retries += 1
        if category_mappings is None:
            msg = "After several retries, the LLM was unable to produce a parsable list of JSON categories for processing.  Processing is failing..."   # pylint: disable=line-too-long
            logger.error(msg)
            raise ValueError(msg)

        # update dataframe with new category column
        new_column_category = []
        for index, row in df.iterrows():        # pylint: disable=unused-variable
            subcategory = row[self.COLUMN_AI_SUBCATEGORY]
            category = self.get_category_for_subcategory(category_mappings, subcategory)
            if category is None:
                logger.warning("Category is unknown - nothing specified for subcategory:  %s",
                               subcategory)
                category = self.UNKNOWN_CATEGORY
            new_column_category.append(category)
        df[self.COLUMN_AI_CATEGORY] = new_column_category

        return df

    def get_category_for_subcategory(self, category_mappings, subcategory):
        """ Gets the category name for the provided subcategory.
        
            category_mappings - category mappings as returned by LLM
            subcategory - subcategory to find
        """
        # handle empty subcategories
        if subcategory is None or len(subcategory) == 0:
            logger.warning("Empty subcategory...  Using default.")
            return None

        # loop through categories
        for category_group in category_mappings:
            if category_group is not None and \
                "category" in category_group and \
                "subcategories" in category_group:
                # check for a match
                category = category_group["category"]
                for s in category_group["subcategories"]:
                    if s == subcategory:
                        return category
            else:
                logger.warning("Unexpected category structure.  Category Group=%s", category_group)

        # no match
        logger.warning("No match found for subcategory.  Subcategory=%s", subcategory)
        return None
