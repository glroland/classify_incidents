""" Automation Agent MCP Server """
import logging
import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastmcp import FastMCP
from starlette.responses import JSONResponse
from tools.research_request import research_request
from tools.create_plan import create_plan
from tools.judge_plan import judge_plan, JudgePlanResponse
from tools.revise_plan import revise_plan
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
mcp_asgi_app = mcp.http_app(path="/")

# Create FastAPI application
app = FastAPI(lifespan=mcp_asgi_app.lifespan)
app.mount("/mcp", mcp_asgi_app)

@app.get("/health")
async def health_check(request):
    """ Health check endpoint for the MCP Server. """
    # check database connection
    return JSONResponse({"status": "ok"})

class ResearchRequest(BaseModel):
    user_request: str
@app.post("/api/research_request", response_class=PlainTextResponse)
async def api_research_request(request: ResearchRequest) -> str:
    return await research_request(request.user_request)

class CreatePlanRequest(BaseModel):
    user_request: str
    research: str
@app.post("/api/create_plan", response_class=PlainTextResponse)
async def api_create_plan(request: CreatePlanRequest) -> str:
    return await create_plan(request.user_request, request.research)

class JudgePlanRequest(BaseModel):
    user_request: str
    research: str
    nominated_plan: str
@app.post("/api/judge_plan", response_class=JSONResponse)
async def api_judge_plan(request: JudgePlanRequest) -> JudgePlanResponse:
    return await judge_plan(request.user_request, request.research, request.nominated_plan)

class RevisePlanRequest(BaseModel):
    feedback: str
    plan: str
@app.post("/api/revise_plan", response_class=PlainTextResponse)
async def api_revise_plan(request: RevisePlanRequest) -> str:
    return await revise_plan(request.feedback, request.plan)

class WriteScript(BaseModel):
    plan: str

@app.post("/api/write_ansible_playbook", response_class=PlainTextResponse)
async def api_write_ansible_playbook(request: WriteScript) -> str:
    return await write_ansible_playbook(request.plan)

@app.post("/api/write_bash_script", response_class=PlainTextResponse)
async def api_write_bash_script(request: WriteScript) -> str:
    return await write_bash_script(request.plan)

@app.post("/api/write_powershell_script", response_class=PlainTextResponse)
async def api_write_powershell_script(request: WriteScript) -> str:
    return await write_powershell_script(request.plan)

class ValidateCodeRequest(BaseModel):
    language: str
    source_code: str
@app.post("/api/validate_code", response_class=PlainTextResponse)
async def api_validate_code(request: ValidateCodeRequest) -> str:
    return await validate_code(request.language, request.source_code)

def main():
    """ Entrypoint for the MCP Server application. """

    # add the tools
    mcp.tool(research_request)
    mcp.tool(create_plan)
    mcp.tool(judge_plan)
    mcp.tool(revise_plan)
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
