from google.adk.agents import LlmAgent

from .prompts import ICP_QUALITY_EVALUATOR_INSTRUCTION
from ..schemas import ICPEvaluationResult

icp_quality_evaluator = LlmAgent(
    name="icp_quality_evaluator",
    model="gemini-2.5-flash",
    description="Evaluates ICP document quality and completeness",
    instruction=ICP_QUALITY_EVALUATOR_INSTRUCTION,
    output_schema=ICPEvaluationResult,
    output_key="icp_evaluation",
)