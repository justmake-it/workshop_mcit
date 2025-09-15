"""
Context Evaluator Agent - Evaluates Company Information Completeness

Key ADK Features Demonstrated:
1. Agent as a tool: Can be used by other agents via AgentTool
2. output_schema: Returns structured evaluation data
3. include_contents='none': Only needs the provided context, no history
4. Focused evaluation: Single responsibility principle
"""

from google.adk.agents import LlmAgent
from ..schemas import ContextEvaluation

# WORKSHOP TEACHING MOMENT: Agent as a Tool Pattern
# -------------------------------------------------
# This agent is designed to be used AS A TOOL by other agents.
# The orchestrator uses AgentTool(agent=context_evaluator) to call this.
# This pattern allows for modular, reusable evaluation logic.

context_evaluator = LlmAgent(
    name="context_evaluator",
    model="gemini-2.5-flash",  # Fast model for quick evaluation
    
    description=(
        "Evaluates company information completeness for ICP development. "
        "Returns structured assessment with scores and recommendations."
    ),
    
    # CRITICAL: Structured output for predictable evaluation
    output_schema=ContextEvaluation,
    
    # Performance optimization: No conversation history needed
    include_contents='none',
    
    # Automatic state management
    output_key="context_evaluation",
    
    instruction="""You evaluate company information completeness for ICP (Ideal Customer Profile) development.

Your evaluation should be based on these criteria:

ESSENTIAL ELEMENTS (Must have for effective ICP):
1. Company Core (40% weight)
   - Company name and what they do
   - Industry/vertical they operate in
   - Basic product/service description

2. Target Market (30% weight)
   - Who they sell to (company size, type)
   - Customer characteristics or segments
   - At least one identified target group

3. Business Model (30% weight)
   - How they make money (pricing, subscription, etc.)
   - Or at least their intended approach

VALUABLE ELEMENTS (Enhance ICP quality):
4. Competitive Position
   - Main competitors identified
   - Key differentiation or unique value

5. Current Status
   - Company stage (pre-seed, seed, etc.)
   - Team size
   - Current traction (customers, revenue)

6. Problem Space
   - Specific pain points addressed
   - Why customers need this

SCORING APPROACH:
- Score each category 0.0 to 1.0
- Company is ready for ICP work if essentials score > 0.7
- Overall completeness = weighted average of all categories

MISSING ELEMENTS:
- Identify top 3 critical gaps that would most improve ICP quality
- Suggest specific questions to fill those gaps

RECOMMENDATION:
- If essentials are strong (>0.7): "Ready for ICP development - proceed to research"
- If essentials are weak (<0.7): "Need more context - gather essential information first"

Example of good context:
"We're AgentFlow AI, a DevOps platform that predicts CI/CD failures. We target gaming studios 
with 100-500 employees. Our SaaS model charges $500-2000/month. Main competitors are Datadog 
(reactive, expensive) and PagerDuty (incident-only)."

Example of insufficient context:
"I'm building a DevOps platform"

Remember: Your evaluation guides whether to proceed with research or gather more context first.
"""
)