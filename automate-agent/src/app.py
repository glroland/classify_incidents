""" Automation Agent MCP Server """
import logging
from fastmcp import FastMCP
from tools.research_request import research_request
from tools.create_plan import create_plan
from tools.judge_plan import judge_plan
from tools.get_source_code import get_source_code
from tools.validate_code import validate_code
from utils.settings import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP()

def main():
    """ Entrypoint for the MCP Server application. """
    # add the tools
    mcp.tool(research_request)
    mcp.tool(create_plan)
    mcp.tool(judge_plan)
    mcp.tool(get_source_code)
    mcp.tool(validate_code)

    # Run the FastMCP app
    mcp.run(transport="sse", host=settings.SERVER_ADDRESS, port=settings.SERVER_PORT)

if __name__ == "__main__":
    main()
