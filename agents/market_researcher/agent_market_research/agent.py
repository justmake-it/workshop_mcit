from google.adk.agents import Agent, LlmAgent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool

from .prompt import COORDINATOR_INSTRUCTION, EXPLORER_INSTRUCTION

# Create the specialized research agent
market_explorer = Agent(
    name="market_explorer",
    model="gemini-2.5-pro",
    description="Research assistant specialized in exploring industries and DevOps challenges",
    instruction=EXPLORER_INSTRUCTION,
    tools=[google_search],
)

# Create the conversation coordinator
coordinator = LlmAgent(
    name="market_research_coordinator",
    model="gemini-2.5-pro",
    description="Facilitates natural research conversations about DevOps market opportunities",
    instruction=COORDINATOR_INSTRUCTION,
    tools=[AgentTool(agent=market_explorer)],
)

# Export the coordinator as the root agent
root_agent = coordinator
