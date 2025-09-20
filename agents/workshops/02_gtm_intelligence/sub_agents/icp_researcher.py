from google.adk.agents import LlmAgent

from .prompts import ICP_RESEARCHER_INSTRUCTION

icp_researcher = LlmAgent(
    name="icp_researcher",
    model="gemini-2.5-flash",
    description="Researches potential target markets and customer segments for ICP development",
    instruction=ICP_RESEARCHER_INSTRUCTION,
    output_key="pipeline_research_findings",
)