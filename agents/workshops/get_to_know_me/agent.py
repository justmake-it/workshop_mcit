from google.adk.agents import LlmAgent

# Import prompt from separate file for better organization
from .prompts import GET_TO_KNOW_ME_INSTRUCTION

get_to_know_me = LlmAgent(
    name="get_to_know_me",
    model="gemini-2.5-flash",
    description="Get to know the user agent",
    instruction=GET_TO_KNOW_ME_INSTRUCTION,
)

root_agent = get_to_know_me
