from google.adk.agents import LlmAgent

from .prompts import ICP_WRITER_INSTRUCTION
from ..schemas import ICPDocument

icp_writer = LlmAgent(
    name="icp_writer",
    model="gemini-2.5-pro",
    description="Creates structured ICP document from research findings",
    instruction=ICP_WRITER_INSTRUCTION,
    output_schema=ICPDocument,
    output_key="icp_document",
)