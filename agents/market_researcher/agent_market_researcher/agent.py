from google.adk.agents import Agent, LlmAgent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool

from .prompts import GREETER_PROMPT, RESEARCH_ASSISTANT_PROMPT, COORDINATOR_PROMPT

# Greeter agent
greeter_agent = Agent(
    name="greeter",
    model="gemini-2.5-pro",
    instruction=GREETER_PROMPT,
    description="Starts conversations about gaming companies",
)

# Research assistant
research_assistant = Agent(
    name="research_assistant",
    model="gemini-2.5-pro",
    instruction=RESEARCH_ASSISTANT_PROMPT,
    description="Researches gaming companies and DevOps challenges",
    tools=[google_search],
)

# Root agent with AgentTool pattern
root_agent = LlmAgent(
    name="market_researcher",
    model="gemini-2.5-pro",
    instruction=COORDINATOR_PROMPT,
    description="Market research coordinator",
    tools=[
        AgentTool(agent=greeter_agent),
        AgentTool(agent=research_assistant),
    ],
)
