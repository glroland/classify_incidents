""" Service Gateway for ServiceNow API Access. """
import logging
from urllib.parse import urlencode
import base64
import requests
from settings import settings

logger = logging.getLogger(__name__)

# pylint: disable=too-few-public-methods
class ServiceNowGateway():
    """ Service Now Service Gateway """

    # constants
    SNOW_BASE_URL = "service-now.com/api/now/"
    HEADER_AUTH = "Authorization"
    HEADER_PREFIX_BASIC_AUTH = "Basic "

    # Service Now Action List
    class ServiceNowActions():
        """ List of SNOW Actions """
        SNOW_INCIDENT_TABLE : str = "table/incident"

    def query_snow(self, parameters : list):
        """ Query Service Now with the given parameter list.
        
            parameters - search parameters
        """

        # pylint: disable=line-too-long
        # API Reference - https://www.servicenow.com/docs/bundle/zurich-api-reference/page/integrate/inbound-rest/concept/c_TableAPI.html

        # REST API Explorer Documentation - https://www.servicenow.com/docs/bundle/xanadu-api-reference/page/integrate/inbound-rest/task/t_GetStartedAccessExplorer.html

        # sysparm_query: This is the most powerful parameter for filtering. You can use encoded query strings to specify conditions (e.g., number=INC0012345, active=true^priority=1). You can build these by filtering a list in ServiceNow and then right-clicking on the filter breadcrumbs to "Copy Query."
        # sysparm_fields: Specify a comma-separated list of fields you want to retrieve (e.g., number,short_description,state).
        # sysparm_limit: Limit the number of records returned.
        # sysparm_offset: Offset the starting record for pagination.
        # sysparm_display_value: Control how reference fields are displayed (e.g., true for display values, false for sys_ids).

        # invoke snow api
        url = self.get_snow_url(self.ServiceNowActions.SNOW_INCIDENT_TABLE, parameters)
        headers = self.build_snow_headers()
        http_response = requests.get(url, headers=headers, timeout=settings.SERVICE_NOW_TIMEOUT)
        if http_response.status_code != 200:
            msg = f"Unable to invoke SNOW API.  HTTP Response Code = {http_response.status_code}"
            logger.error(msg)
            raise ValueError(msg)
        json_response = http_response.json()

        logger.info("JSON Resposne from ServiceNow Query = %s", json_response)
        return json_response

    def get_snow_url(self, action : str, parameters : list[dict]) -> str:
        """ Builds the Service Now URL for the provided action. 
        
            action - service now action to perform
            parameters - list of key value pairs to include in request url
        """
        # validate action
        if action is None or len(action) == 0:
            msg = "Input action is empty but required!"
            logger.error(msg)
            raise ValueError(msg)

        # validate configuration
        instance = settings.SERVICE_NOW_INSTANCE
        if instance is None or len(instance) == 0:
            msg = "Configured ServiceNow Instance ID is empty but required!"
            logger.error(msg)
            raise ValueError(msg)

        # build url
        url = "https://" + instance + "." + self.SNOW_BASE_URL + action
        if parameters is not None and len(parameters) > 0:
            url += urlencode(parameters)
        logger.debug("ServiceNow URL for action '%s' and parameters '%s' = %s", \
                     action, parameters, url)

        return url

    def build_snow_headers(self) -> dict:
        """ Builds a list of headers to include in the ServiceNow request. """
        # validate configuration
        if settings.SERVICE_NOW_USERNAME is None or len(settings.SERVICE_NOW_USERNAME) == 0:
            msg = "Service Now Username is empty but required!"
            logger.error(msg)
            raise ValueError(msg)
        if settings.SERVICE_NOW_PASSWORD is None or len(settings.SERVICE_NOW_PASSWORD) == 0:
            msg = "Service Now Password is empty but required!"
            logger.error(msg)
            raise ValueError(msg)

        # encode base auth string
        user_pass = settings.SERVICE_NOW_USERNAME + ":" + settings.SERVICE_NOW_PASSWORD
        user_pass_bytes = user_pass.encode('utf-8')
        user_pass_base64 = base64.b64encode(user_pass_bytes)
        user_pass_base64_str = user_pass_base64.decode('ascii')

        headers = {}

        # add authorization header
        headers[self.HEADER_AUTH] = self.HEADER_PREFIX_BASIC_AUTH + " " + user_pass_base64_str

        logger.debug("SNOW Headers: %s", headers)
        return headers
