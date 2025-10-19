""" Web Command for Importing Incidents from an Object Store. """
import os
import logging
from pathlib import Path
from pydantic import BaseModel, ConfigDict
import pandas as pd
from commands.from_string import FromStringCommand
from gateways.object_storage_gateway import ObjectStorageGateway

logger = logging.getLogger(__name__)

class FromSpaceCommand(BaseModel):
    """ Command processor for the From Space action in the web front end."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    # constants
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
                                       "Summary",
                                       "Subcategory",
                                       "Is_Manual",
                                       "Is_Outage",
                                       "Status"
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
                                       command.summary,
                                       command.category,
                                       command.is_manual,
                                       command.is_outage,
                                       command.status
                                       ]

        self.analysis = df

        # save analysis as a CSV
        analysis_csv = df.to_csv(index=False)
        gateway.upload(f"{self.space_id}/analysis.csv", analysis_csv)
