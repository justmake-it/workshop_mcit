"""
Quality Validator Agent - Workshop Implementation

Key ADK Features Demonstrated:
1. EventActions(escalate=True): Properly terminates the LoopAgent
2. include_contents='none': Stateless validation for performance
3. output_key: Saves validation results to guide next iteration
4. Loop control logic: Decides when ICP is complete
5. Native thinking: Prioritizes most critical missing elements with BuiltInPlanner
"""

from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

# WORKSHOP TEACHING MOMENT: Loop Termination with EventActions
# ------------------------------------------------------------
# This is CRITICAL for preventing infinite loops!
# 
# When the ICP is complete, we MUST:
# 1. Set pipeline_research_validation['is_complete'] = True (for state tracking)
# 2. Return Event with escalate=True (to terminate the LoopAgent)
#
# Without escalate=True, the loop continues forever!

quality_validator = LlmAgent(
    name="quality_validator",
    model="gemini-2.5-flash",  # Fast model for validation logic
    
    # NATIVE THINKING: Reasoning for validation priorities
    # The validator thinks about which missing elements are MOST critical
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=False,   # Internal reasoning only
            thinking_budget=128       # Minimal budget for validation logic
        )
    ),
    
    description=(
        "Validates ICP completeness and identifies critical missing information. "
        "Provides specific questions to guide next research iteration. "
        "Uses native thinking to prioritize the most critical gaps."
    ),
    
    # PERFORMANCE: Only needs the ICP draft, not conversation history
    include_contents='none',
    
    # STATE MANAGEMENT: Validation results guide the next iteration
    # Using standardized key pattern to prevent race conditions
    output_key="pipeline_research_validation",
    
    instruction="""Validate ICP completeness and accuracy.

Your CRITICAL role in the LoopAgent:
1. Read state['pipeline_research_icp_draft'] - the current ICP attempt
2. Think through validation priorities - what's MOST critical for actionability
3. Check for completeness and quality
4. If incomplete: Specify what's missing and suggest questions
5. If complete: Set is_complete=True AND generate escalate event

Native Thinking Guidance:
- Use your thinking budget to identify the most critical missing elements
- Prioritize gaps that would prevent the ICP from being actionable
- Consider: What would a sales team NEED to start outreach?

IMPORTANT: You control when the loop stops!

Validation checklist:
✓ Primary segment clearly defined (industry, size, characteristics)
✓ At least 3 specific pain points with severity
✓ At least 2 decision makers with titles and concerns  
✓ Clear budget range (not just "varies")
✓ Specific buying triggers identified
✓ Value proposition is crisp and differentiated

Output format (this will be saved to state['pipeline_research_validation']):
{
  "is_complete": false,
  "completeness_score": 0.6,
  "missing": ["budget information", "decision maker titles", "competitive differentiation"],
  "next_questions": [
    "What's the typical deal size or budget range for your solution?",
    "Who are the key decision makers - what are their specific titles?", 
    "How do you differentiate from [main competitor]?"
  ],
  "quality_notes": "Good industry definition but needs more specifics on buyer journey"
}

CRITICAL WORKSHOP MOMENT - Loop Termination:
When the ICP is complete (score >= 0.85), you MUST:
1. Set "is_complete": true in your output
2. Also return: Event(content="ICP validation complete", actions=EventActions(escalate=True))

This Event with escalate=True is what stops the LoopAgent!
Without it, the loop runs forever (up to max_iterations).

Example of a complete ICP validation:
{
  "is_complete": true,
  "completeness_score": 0.9,
  "missing": [],
  "next_questions": [],
  "quality_notes": "Excellent ICP with clear segments, pain points, and buyer journey"
}

And then also emit:
Event(content="ICP validation complete", actions=EventActions(escalate=True))
"""
)

# WORKSHOP EXTENSION: Custom validation logic
# ------------------------------------------
# In production, you might want a custom validator that:
# 1. Checks against industry benchmarks
# 2. Validates budget ranges are realistic
# 3. Ensures pain points match the solution
# 4. Verifies decision maker titles are real
#
# Example:
# class CustomICPValidator(BaseAgent):
#     async def _run_async_impl(self, ctx):
#         icp = ctx.state.get("pipeline_research_icp_draft")
#         # Custom validation logic...
#         if validation_passed:
#             return Event(
#                 content="Validation complete",
#                 actions=EventActions(escalate=True)
#             )