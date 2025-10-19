""" Web Command for Importing Incidents from an Object Store. """
import os
import logging
import json
from pathlib import Path
from pydantic import BaseModel, ConfigDict
import pandas as pd
from commands.from_string import FromStringCommand
from gateways.inference_gateway import InferenceGateway
from gateways.object_storage_gateway import ObjectStorageGateway
from utils.get_prompt import prompts

logger = logging.getLogger(__name__)

class FromSpaceCommand(BaseModel):
    """ Command processor for the From Space action in the web front end."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    # constants
    COLUMN_AI_CATEGORY : str = "Category"
    COLUMN_AI_SUBCATEGORY : str = "Subcategory"
    UNKNOWN_CATEGORY : str = "Unspecified by AI"

    # config
    MAX_RETRIES : int = 5
    files_to_skip : list[str] = []

    # input parameters
    space_id : str = None

    # output parameters
    analysis : pd.DataFrame = None

    def go(self):
        """ Execute the command. """
        # validate input path
        logger.debug("space_id: %s", self.space_id)
        if self.space_id is None or len(self.space_id) == 0:
            msg = "Space ID is a Required Value and Cannot be Empty!"
            logger.error(msg)
            raise ValueError(msg)

        gateway = ObjectStorageGateway()

        # list files in space
        raw_files = []
        all_files = gateway.list()
        for file in all_files:
            # break the file into parts
            path_object = Path(file)
            parts = path_object.parts

            if parts is not None and \
                len(parts) == 3 and \
                parts[0] == self.space_id and \
                parts[1] == "raw":
                raw_files.append(file)

        # validate that at least one file exists
        if len(raw_files) == 0:
            msg = f"No files exist in space/raw: {self.space_id}"
            logger.error(msg)
            raise ValueError(msg)
        logger.info("# of files found in space '%s': %s", self.space_id, len(raw_files))

        df = pd.DataFrame([], columns=["Incident_File", 
                                       "Row",
                                       "Asset",
                                       "Summary",
                                       "Subcategory",
                                       "Is_Manual",
                                       "Is_Outage",
                                       "Status",
                                       "Date_Reported",
                                       "Date_Resolved"
                                       ])

        # process each file
        for file in raw_files:
            if os.path.basename(file) in self.files_to_skip:
                logger.warning("Skipping file...   Filename=%s", file)
            else:
                logger.info("Processing file: %s", file)

                # load file
                logger.info("Loading File: %s", file)
                contents = gateway.download(file)

                # process each line in th efile
                contents_lines = contents.splitlines()
                row_index : int = 0
                for line in contents_lines:
                    row_index += 1

                    # execute file processing command
                    command = FromStringCommand()
                    command.input_str = line
                    command.go()

                    # append row
                    df.loc[len(df)] = [file,
                                       row_index,
                                       command.asset_name,
                                       command.summary,
                                       command.category,
                                       command.is_manual,
                                       command.is_outage,
                                       command.status,
                                       command.date_reported,
                                       command.date_resolved
                                       ]

        # Augment data frame with new column for category
        df = self.generalize_subcategories(df)

        self.analysis = df

        # save analysis as a CSV
        analysis_csv = df.to_csv(index=False)
        gateway.upload(f"{self.space_id}/analysis.csv", analysis_csv)


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
            categories_json_str = None
            try:
                categories_json_str = gateway.simple_chat(prompts.ROLLUP_SUBCATEGORIES,
                                                          subcategories_csv)
                logger.debug("Categories from Subcategories Response == %s", categories_json_str)
                category_mappings = json.loads(categories_json_str)

                if category_mappings is not None:
                    break
            except Exception as e:  # pylint: disable=broad-exception-caught
                logger.warning("An error occurred while trying to create generalized categories list.  Retrying...  Exception=%s.  JSON_String=%s", e, categories_json_str)   # pylint: disable=line-too-long
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

        # change order of columns
        columns = df.columns.tolist()
        columns.remove(self.COLUMN_AI_CATEGORY)
        subcategory_index = columns.index(self.COLUMN_AI_SUBCATEGORY)
        columns.insert(subcategory_index, self.COLUMN_AI_CATEGORY)
        df = df[columns]

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
