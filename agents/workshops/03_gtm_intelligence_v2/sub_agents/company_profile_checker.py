from google.adk.agents import LlmAgent

from ..schemas import Feedback

PROFILE_CHECKER_INSTRUCTION = """
Evaluate if the company profile below has all required information for ICP research.

## COMPANY PROFILE TO EVALUATE:
{company_profile}

## EVALUATION RULES:
Check ALL 7 required fields:
1. company_name: NOT empty string ""
2. industry: NOT empty string ""
3. company_stage: NOT empty string ""
4. team_size: NOT empty string ""
5. core_offering: NOT empty string ""
6. key_differentiators: NOT empty list []
7. current_challenges: NOT empty list []

- PASS: ALL 7 fields have values
- FAIL: ANY field is empty

## EXAMPLES:
Pass example:
{"grade": "pass", "comment": "All required fields present: AgentFlow AI (B2B SaaS, pre-seed, 2 people) with clear differentiators and challenges.", "follow_up_queries": null}

Fail example:
{"grade": "fail", "comment": "Missing: team_size (empty string), current_challenges (empty list)", "follow_up_queries": ["How many people are currently on your team?", "What are your top 1-2 concrete business or technical challenges?"]}

## FOLLOW-UP QUESTIONS FOR MISSING FIELDS:
- company_name: "What's your company name?"
- industry: "What specific industry or vertical does your company operate in?"  
- company_stage: "What stage is your company at (pre-seed, seed, Series A, growth, etc.)?"
- team_size: "How many people are currently on your team?"
- core_offering: "Can you describe specifically what your product/service does?"
- key_differentiators: "What specific features or metrics make your product different from competitors?"
- current_challenges: "What are your top 1-2 concrete business or technical challenges?"

Your response must be a single, raw JSON object validating against the 'Feedback' schema.
"""

company_profile_checker = LlmAgent(
    name="profile_completeness_checker",
    model="gemini-2.5-flash",
    description="Evaluates company profile completeness",
    instruction=PROFILE_CHECKER_INSTRUCTION,
    output_schema=Feedback,
    output_key="company_profile_evaluation",
)