import os
import logging
from pydantic import BaseModel
from from_file_command import FromFileCommand

logger = logging.getLogger(__name__)

class FromDirectoryCommand(BaseModel):
    """ Command processor for the From Directory action in the CLI."""

    # input parameters
    input_path : str = None

    def go(self):
        """ Execute the command. """
        # validate input path
        logger.debug("Input Path: %s", self.input_path)
        if self.input_path is None or len(self.input_path) == 0:
            msg = "Input Path is a Required Value and Cannot be Empty!"
            logger.error(msg)
            raise ValueError(msg)
        if not os.path.exists(self.input_path):
            msg = f"Input Path does not exist!  Path={self.input_path}"
            logger.error(msg)
            raise ValueError(msg)
        if not os.path.exists(self.input_path):
            msg = f"Input Path does not exist!  Path={self.input_path}"
            logger.error(msg)
            raise ValueError(msg)
        if not os.path.isdir(self.input_path):
            msg = f"Input Path exists but is not a directory!  Path={self.input_path}"
            logger.error(msg)
            raise ValueError(msg)
        abs_path = os.path.abspath(self.input_path)
        logger.info("Input Path (Absolute): %s", abs_path)

        # get a list of all files in directory
        file_list = self.get_all_files_in_directory_recursively(abs_path)
        if len(file_list) == 0:
            logger.warning("Path contains no files!  Path=%s", abs_path)
            return

        # process each file
        for file in file_list:
            logger.info("Processing file: %s", file)
            command = FromFileCommand()
            command.filename_w_path = file
            command.go()


    def get_all_files_in_directory_recursively(self, path):
        """ Gets all files in the specified directory.  Recursively walks tree. 

            path - directory to search
        """
        file_list = []

        for root, _, files in os.walk(path):
            for file in files:
                file_list.append(os.path.join(root, file))

        return file_list
