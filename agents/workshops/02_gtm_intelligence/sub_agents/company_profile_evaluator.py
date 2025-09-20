from google.adk.agents import LlmAgent

from .prompts import GTM_COMPANY_PROFILE_EVALUATOR
from ..schemas import EvaluationResult

company_profile_evaluator = LlmAgent(
    name="company_profile_evaluator",
    model="gemini-2.5-flash",
    description="Evaluates company information completeness for ICP development for other agents in the system.",
    instruction=GTM_COMPANY_PROFILE_EVALUATOR,
    output_schema=EvaluationResult,
    output_key="context_evaluation",
)
