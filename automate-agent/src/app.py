""" Automation Agent MCP Server """
import logging
import uvicorn
from fastapi import FastAPI
from fastmcp import FastMCP
from starlette.responses import JSONResponse
from tools.research_request import research_request
from tools.create_plan import create_plan
from tools.judge_plan import judge_plan
from tools.write_ansible_playbook import write_ansible_playbook
from tools.write_bash_script import write_bash_script
from tools.write_powershell_script import write_powershell_script
from tools.validate_code import validate_code
from utils.settings import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create ASGI-based FastMCP application
mcp = FastMCP("Automate IT Agent", stateless_http=True)
mcp_asgi_app = mcp.http_app()

# Create FastAPI application
app = FastAPI()
app.mount("/mcp", mcp_asgi_app)

@app.get("/health")
async def health_check(request):
    """ Health check endpoint for the MCP Server. """
    # check database connection
    return JSONResponse({"status": "ok"})

@app.get("/api/research_request")
async def api_research_request(user_request: str) -> str:
    return await research_request(user_request)

@app.get("/api/create_plan")
async def api_create_plan(user_request: str, research: str) -> str:
    return await create_plan(user_request, research)

@app.get("/api/judge_plan")
async def api_judge_plan(user_request: str, research: str, nominated_plan: str) -> str:
    return await judge_plan(user_request, research, nominated_plan)

@app.get("/api/write_ansible_playbook")
async def api_write_ansible_playbook(plan: str) -> str:
    return await write_ansible_playbook(plan)

@app.get("/api/write_bash_script")
async def api_write_bash_script(plan: str) -> str:
    return await write_bash_script(plan)

@app.get("/api/write_powershell_script")
async def api_write_powershell_script(plan: str) -> str:
    return await write_powershell_script(plan)

@app.get("/api/validate_code")
async def api_validate_code(language: str, source_code: str) -> str:
    return await validate_code(language, source_code)

def main():
    """ Entrypoint for the MCP Server application. """
    # add the tools
    mcp.tool(research_request)
    mcp.tool(create_plan)
    mcp.tool(judge_plan)
    mcp.tool(write_ansible_playbook)
    mcp.tool(write_bash_script)
    mcp.tool(write_powershell_script)
    mcp.tool(validate_code)

    # Run the FastMCP app
    if settings.NUM_WORKERS <= 0:
        uvicorn.run(app,
                    host=settings.SERVER_ADDRESS,
                    port=settings.SERVER_PORT,
                    log_config=None)
    else:
        uvicorn.run("app:app",
                    host=settings.SERVER_ADDRESS,
                    port=settings.SERVER_PORT,
                    workers=settings.NUM_WORKERS,
                    log_config=None)

if __name__ == "__main__":
    main()
