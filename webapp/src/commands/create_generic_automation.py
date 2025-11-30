""" Command for create generic automation (i.e. automation playground). """
import logging
import json
import requests
from pydantic import BaseModel
from gateways.inference_gateway import InferenceGateway
from utils.settings import settings

logger = logging.getLogger(__name__)

class GenerateCodeResponse():
    language : str
    filename : str
    source_code : str

class CreateGenericAutomationCommand:
    """ Command processor for the Create Generic Automation action."""

    MAX_CORRECTION_CYCLES = 3

    # input parameters
    prompt: str
    placeholder = None
    fn_update_status = None
    fn_output_markdown = None
    fn_output_code = None
    fn_artifact = None

    # results
    implementation_plan: str
    class File(BaseModel):
        filename: str
        source_code: str
    artifacts: list[File] = []

    def go(self):
        """ Processes a user prompt to create automation.
        
            prompt - user request
            placeholder - streamlit placeholder widget
        """
        # Research Request
        self.fn_update_status(self.placeholder, "Researching request...")
        payload = {
            "user_request": self.prompt,
        }
        research = self.invoke_api("research_request", payload)
        self.fn_output_markdown("See research", research)

        # Create Implementation Plan
        self.fn_update_status(self.placeholder, "Research complete.  Creating implementation plan...")
        payload = {
            "user_request": self.prompt,
            "research": research,
        }
        nominated_plan = self.invoke_api("create_plan", payload)
        self.fn_output_markdown("See implementation plan", nominated_plan)

        correction_count = 0
        while (correction_count < self.MAX_CORRECTION_CYCLES):
            # Judge Implementation Plan
            if correction_count == 0:
                self.fn_update_status(self.placeholder, "Implementation plan created.  Obtaining a peer review from a judge...")
            else:
                self.fn_update_status(self.placeholder, f"Received negative feedback on plan from judge.  Modifying plan...  (Cycle #{correction_count+1})")
            payload = {
                "user_request": self.prompt,
                "research": research,
                "nominated_plan": nominated_plan,
            }
            feedback_on_plan_str = self.invoke_api("judge_plan", payload)
            feedback_on_plan = json.loads(feedback_on_plan_str)
            feedback_on_plan_display = "# "
            if feedback_on_plan["revise_plan_flag"]:
                feedback_on_plan_display += "Revisions Required\n"
            else:
                feedback_on_plan_display += "Quality Plan\n"
            feedback_as_str = "\nSpecific Feedback:\n"
            feedback_counter = 1
            for feedback in feedback_on_plan["feedback"]:
                feedback_on_plan_display += f"* {feedback}\n"
                feedback_as_str += f"{feedback_counter}.) {feedback}\n"
                feedback_counter += 1
            self.fn_output_markdown("See feedback on plan after AI review", feedback_on_plan_display)

            # Determine if plan revision is necessary
            if feedback_on_plan["revise_plan_flag"]:
                payload = {
                    "feedback": feedback_as_str,
                    "plan": nominated_plan,
                }
                nominated_plan = self.invoke_api("revise_plan", payload)
                self.fn_output_markdown("See revised plan based on criticisms from judge", nominated_plan)
            else:
                break

            correction_count += 1
        self.implementation_plan = nominated_plan

        # Write Source Code
        self.fn_update_status(self.placeholder, "Writing script based on the final implementation plan...")
        source_code_response = self.generate_code(self.implementation_plan)
        self.fn_artifact(source_code_response.language, source_code_response.source_code)

        # Validate Source Code
        self.fn_update_status(self.placeholder, "Performing a code review of the generated source code...")
        payload = {
            "language": source_code_response.language,
            "source_code": source_code_response.source_code,
        }
        code_review_feedback = self.invoke_api("validate_code", payload)
        self.fn_output_code("See code review feedback", code_review_feedback)

        # Create Artifacts
        artifact = self.File(filename = source_code_response.filename,
                             source_code = source_code_response.source_code)
        self.artifacts.append(artifact)

        self.fn_update_status(self.placeholder, ":green[*Completed Successfully!*]")


    def get_mcp_servers_list(self, allowed_tools):
        """ Dynamically generate MCP Server Tool for OpenAI Responses API
        
            allowed_tools - list of allowed tool calls within MCP server

            Returns: list of MCP Servers
        """
        mcp_servers_list = []

        if allowed_tools is None or len(allowed_tools) == 0:
            mcp_servers_list.append(
                # Automate IT Agent
                {
                    "type": "mcp",
                    "server_label": "automate-agent",
                    "server_url": settings.AUTOMATE_AGENT_URL,
                    "require_approval": "never",
                }
            )
        else:
            mcp_servers_list.append(
                # Automate IT Agent
                {
                    "type": "mcp",
                    "server_label": "automate-agent",
                    "server_url": settings.AUTOMATE_AGENT_MCP_URL,
                    "require_approval": "never",
                    "allowed_tools": allowed_tools,
                }
            )

        #research_request
        #create_plan
        #judge_plan
        #write_ansible_playbook
        #write_bash_script
        #write_powershell_script
        #validate_code

        return mcp_servers_list


    def invoke_api(self, api_name, payload):
        url = settings.AUTOMATE_AGENT_API_URL + "/" + api_name
        headers = {
            "Content-Type": "application/json"
        }
        http_response = requests.post(url, json=payload, headers=headers, timeout=settings.API_TIMEOUT)
        if http_response.status_code != 200:
                msg = f"Unable to invoke Automation Agent API.  HTTP Response Code = {http_response.status_code}.  Content = {http_response.text}"
                logger.error(msg)
                raise ValueError(msg)
        data = http_response.text
        logging.info("API Invoke Response: '%s'", data)
        return data

    def generate_code(self, plan: str) -> GenerateCodeResponse:
        prompt = """
            You are an AI Agent that manages software developer AI Agents that specialize in particular
            programming languages, as indicated by their tool names in the provided MCP Servers list.
            An implementation plan will be provided in the user input.  Your job is to route this plan to the
            correct software developer agent, execute the tool call, then return the results in JSON format.

            Response Structure Example 1:
            {
                "language": "bash",
                "filename": "hello_world.sh",
                "source_code": ".... source code ...."
            }

            Response Structure Example 2:
            {
                "language": "powershell",
                "filename": "current_date.ps1",
                "source_code": ".... source code ...."
            }

            Response Structure Example 3:
            {
                "language": "ansible",
                "filename": "reboot_vm.yaml",
                "source_code": ".... source code ...."
            }

            Language will be provided by the implementation plan.
            Source Code will be provided by the MCP Server tool call.
            Filename is created by you based on the purpose of the script.

            Do not include anything before or after the JSON response.  Your response
            will be directly processed by a JSON parser with no adjustments.
                """

        gateway = InferenceGateway()
        tools = self.get_mcp_servers_list(["write_ansible_playbook", "write_bash_script", "write_powershell_script"])
        result_obj = gateway.json_chat(settings.OPENAI_MODEL, prompt, plan, tools)

        response = GenerateCodeResponse()
        response.language = result_obj["language"]
        response.filename = result_obj["filename"]
        response.source_code = result_obj["source_code"]
        return response
