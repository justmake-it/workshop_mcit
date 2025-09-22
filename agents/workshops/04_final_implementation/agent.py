from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

from .prompts import GTM_COORDINATOR_INSTRUCTION
from .sub_agents import orchestrator_market_researcher, orchestrator_content_creator, orchestrator_outreach_specialist

# Main conversation router with strict routing enforcement
gtm_coordinator = LlmAgent(
    name="gtm_coordinator",
    model="gemini-2.5-pro",
    description="GTM intelligence system that routes to specialized agents for market research, content creation, and outreach planning",
    instruction=GTM_COORDINATOR_INSTRUCTION,
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(include_thoughts=True, thinking_budget=-1)
    ),
    sub_agents=[orchestrator_market_researcher, orchestrator_content_creator, orchestrator_outreach_specialist],
)

root_agent = gtm_coordinator