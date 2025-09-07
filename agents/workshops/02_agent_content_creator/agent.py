from google.adk.agents import LlmAgent

from .prompt import COORDINATOR_INSTRUCTION

# Create the conversation coordinator
coordinator = LlmAgent(
    name="content_creator_coordinator",
    model="gemini-2.5-pro",
    description="Turns ICP insights into compelling campaigns, messaging, and content assets to help founders tell the right story",
    instruction=COORDINATOR_INSTRUCTION,
)

# Export the coordinator as the root agent
root_agent = coordinator
