""" Command for Getting an existing Evaluation Space in web UI. """
import logging
import os
from pathlib import Path
from pydantic import BaseModel, ConfigDict
import pandas as pd
from io import StringIO
from metadata.evaluation_space import EvaluationSpaceMetadata
from metadata.data_file import DataFile
from gateways.object_storage_gateway import ObjectStorageGateway

logger = logging.getLogger(__name__)

class LoadSpacesCommand(BaseModel):
    """ Command processor for the Load Evaluation Space action."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    # input parameters
    space_id : str = None

    # output responses
    metadata : EvaluationSpaceMetadata = None
    analysis_filename : str = None
    analysis_df : pd.DataFrame = None
    raw_data_files : list[DataFile] = []

    def go(self):
        """ Execute the command. """
    
        # validate input parameters
        if self.space_id is None or len(self.space_id) == 0:
            msg = "space_id is a required query parameter but is empty!"
            logger.error(msg)
            raise ValueError(msg)

        # get space metadata from object storage
        gateway = ObjectStorageGateway()
        path = f"{self.space_id}/metadata.json"
        metadata_str = gateway.download(path) 
        self.metadata = EvaluationSpaceMetadata.model_validate_json(metadata_str)

        # populate file lists associated with space
        all_files = gateway.list()
        for file in all_files:
            # break the file into parts
            path_object = Path(file)
            parts = path_object.parts

            # find space
            if parts is not None and len(parts) > 0 and parts[0] == self.space_id:
                if len(parts) == 2:
                    if parts[1].lower() == "analysis.csv":
                        self.analysis_filename = file

                if len(parts) >= 3:

                    # create data file object
                    if parts[1] == "raw":
                        data_file = DataFile()
                        data_file.filename = parts[2]
                        data_file.path = os.path.dirname(file)
                        data_file.parts = parts
                        self.raw_data_files.append(data_file)

        # load analysis, if exists
        if self.analysis_filename is not None and len(self.analysis_filename) > 0:
            analysis_csv = gateway.download(self.analysis_filename)
            analysis_csv_s = StringIO(analysis_csv)
            self.analysis_df = pd.read_csv(analysis_csv_s)
