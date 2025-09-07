from google.adk.agents import Agent

root_agent = Agent(
    name="root_agent",
    model="gemini-2.0-flash",
    description=("Agent to answer general purpose questions about life"),
    instruction=("You are helpful agent who can answer any general purpose question"),
)
