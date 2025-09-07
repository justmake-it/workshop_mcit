from google.adk.agents import LlmAgent

from .prompt import COORDINATOR_INSTRUCTION

# Create the conversation coordinator
gtm_coordinator = LlmAgent(
    name="gtm_coordinator",
    model="gemini-2.5-pro",
    description="",
    instruction=COORDINATOR_INSTRUCTION,
)
