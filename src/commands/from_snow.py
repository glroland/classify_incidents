""" CLI Command for Analyzing Incidents directly from Service Now. """
import logging
import json
from datetime import date, timedelta
from pydantic import BaseModel
from gateways.snow_gateway import ServiceNowGateway
from gateways.object_storage_gateway import ObjectStorageGateway

logger = logging.getLogger(__name__)

class FromServiceNowCommand(BaseModel):
    """ Command processor for the From SNOW action in the CLI."""

    # input parameters
    space_id : str = None
    min_create_date : date = None
    max_create_date : date = None
    row_limit : int = -1

    def go(self):
        """ Execute the command. """
        # validate parameters
        if self.space_id is None or len(self.space_id) == 0:
            msg = "Space ID is a required field but is empty!"
            logger.error(msg)
            raise ValueError(msg)
        if self.min_create_date is None and self.max_create_date is None:
            msg = "At least one filter parameter must be specifiied and all are empty!"
            logger.error(msg)
            raise ValueError(msg)
        if self.row_limit is None or self.row_limit < -1:
            msg = f"Invalid row limit provided: {self.row_limit}"
            logger.error(msg)
            raise ValueError(msg)

        gateway = ServiceNowGateway()

        # build query
        query = ""
        if self.min_create_date is not None:
            query += gateway.SNOW_FILTER_CREATE_DATE + ">=" + gateway.date_to_string(self.min_create_date)
        if self.max_create_date is not None:
            if len(query) > 0:
                query += "&"
            query += gateway.SNOW_FILTER_CREATE_DATE + "<" + gateway.date_to_string(self.max_create_date + timedelta(days=1))
        logger.info("SNOW Query: %s", query)

        # build parameters list
        parameters = {}
        parameters[gateway.SNOW_QUERY] = query
        if self.row_limit is not None and self.row_limit > 0:
            parameters[gateway.SNOW_LIMIT] = str(self.row_limit)

        # query service now
        results = gateway.query_snow(parameters)
        logger.debug("SNOW Query Results: %s", results)

        self.push_to_object_storage(results["result"])

    def push_to_object_storage(self, results):
        """ Save the provided data set back to object storage.

            results - service now query output
        """
        # validate inputs
        if results is None or len(results) == 0:
            msg = "Cannot save empty result set from Service Now!"
            logger.error(msg)
            raise ValueError(msg)

        # build filename
        today = date.today().strftime("%m-%d-%Y")
        filename = f"snow_query_{today}"
        if self.min_create_date is not None:
            filename += "_from_" + self.min_create_date.strftime("%m-%d-%Y")
        if self.max_create_date is not None:
            filename += "_to_" + self.max_create_date.strftime("%m-%d-%Y")
        if self.row_limit is not None and self.row_limit > 0:
            filename += "_limit_" + str(self.row_limit)

        # beautify json
        #results_str = json.dumps(results, indent=4)

        # create jsonl
        jsonl = ""
        for row in results:
            jsonl += json.dumps(row) + "\n"

        # upload file
        gateway = ObjectStorageGateway()
        path = f"{self.space_id}/raw/{filename}.jsonl"
        gateway.upload(path, jsonl)
