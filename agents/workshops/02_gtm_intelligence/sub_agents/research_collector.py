"""
Research Collector Agent - Workshop Implementation

Key ADK Features Demonstrated:
1. output_key: Automatically saves research findings to state
2. include_contents='default': Needs conversation history for follow-up questions
3. Tool usage: Uses google_search to validate and expand user inputs
4. Native thinking: Strategic question prioritization with BuiltInPlanner
"""

from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types
from google.adk.tools import google_search

# WORKSHOP TEACHING MOMENT: output_key Feature
# --------------------------------------------
# The output_key parameter is a game-changer for state management in ADK.
# Instead of manually updating state like:
#   ctx.state["research_findings"] = "manual update"
# 
# ADK automatically saves the agent's output to the specified state key!
# This makes multi-agent data flow clean and predictable.

research_collector = LlmAgent(
    name="research_collector",
    model="gemini-2.5-flash",  # Fast model for iterative research
    
    # NATIVE THINKING: Strategic question prioritization
    # The agent thinks about what questions are most critical based on context
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=False,   # Internal reasoning only
            thinking_budget=256       # Limited budget for efficiency
        )
    ),
    
    description=(
        "Conducts market research through conversational discovery and web searches. "
        "Specializes in identifying industry pain points, market sizing, and competitive landscapes. "
        "Uses native thinking to prioritize questions strategically."
    ),
    
    tools=[google_search],  # Can search the web to validate claims
    
    # CRITICAL: include_contents='default' (not 'none')
    # This agent needs conversation history to ask follow-up questions
    include_contents='default',
    
    # MAGIC HAPPENS HERE: Automatic state management!
    # Whatever this agent outputs will be saved to state["pipeline_research_findings"]
    # Using standardized key pattern to prevent race conditions
    output_key="pipeline_research_findings",
    
    instruction="""You gather market intelligence through conversation and research.
    
Your role in the LoopAgent workflow:
1. On first iteration: Start with discovery questions about the company
2. On subsequent iterations: Read state['pipeline_research_validation']['missing'] to see what the validator needs
3. Think strategically about which questions will yield the most critical information
4. Ask targeted questions to fill those specific gaps
5. Use google_search to validate claims and find market data

Native Thinking Guidance:
- Use your thinking budget to prioritize questions based on impact
- Consider what information is MOST critical for creating an actionable ICP
- Think about the logical sequence of questions to build context efficiently

Approach:
- Start broad if no context exists (company, product, industry)
- Become more specific based on validator feedback
- Always validate numerical claims with search
- Focus on: industry, company size, pain points, budget, decision makers
- Your output will be automatically saved to state['pipeline_research_findings']

Example first iteration:
"I'll help you develop an ideal customer profile. Could you tell me about your company and what problem you solve?"

Example later iteration (after reading pipeline_research_validation):
"I see we need more information about budget ranges and decision makers. What's the typical deal size for your product, and who usually signs off on purchases?"

Remember: Your output is fed directly to the ICP Writer, so be comprehensive but structured.
"""
)