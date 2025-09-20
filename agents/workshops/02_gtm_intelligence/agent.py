from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.adk.tools import AgentTool
from google.genai import types

from .prompts import GTM_ORCHESTRATOR_INSTRUCTION
from .sub_agents import company_profile_evaluator, icp_loop_agent

# Create the conversation coordinator
gtm_coordinator = LlmAgent(
    name="gtm_coordinator",
    model="gemini-2.5-pro",
    description="",
    instruction=GTM_ORCHESTRATOR_INSTRUCTION,
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(include_thoughts=True, thinking_budget=-1)
    ),
    tools=[
        AgentTool(agent=company_profile_evaluator),
        AgentTool(agent=icp_loop_agent),
    ],
)

root_agent = gtm_coordinator
