"""
ICP Writer Agent - Workshop Implementation

Key ADK Features Demonstrated:
1. output_schema: Returns structured data instead of free text
2. include_contents='none': Stateless for 2-3x performance boost
3. output_key: Automatically saves structured ICP to state
4. No tools: Respects ADK's tools OR schemas constraint
"""

from google.adk.agents import LlmAgent
from ..schemas import ICPSchema

# WORKSHOP TEACHING MOMENT: include_contents Performance Optimization
# ------------------------------------------------------------------
# This is a CRITICAL performance optimization in ADK!
# 
# include_contents='default': Agent gets full conversation history (slower)
# include_contents='none': Agent only gets current input + state (faster)
#
# For pure transformation tasks like this, 'none' gives 2-3x speedup
# because the agent doesn't process unnecessary conversation history.

icp_writer = LlmAgent(
    name="icp_writer", 
    model="gemini-2.5-flash",  # Fast model for structured transformation
    description=(
        "Transforms unstructured market research into structured Ideal Customer Profiles "
        "with segments, pain points, decision makers, and buying triggers."
    ),
    
    # CRITICAL: Structured output instead of free text
    # This ensures consistent, parseable results every time
    output_schema=ICPSchema,
    
    # PERFORMANCE BOOST: Stateless transformation
    # This agent doesn't need conversation history - just the research findings
    include_contents='none',
    
    # AUTOMATIC STATE MANAGEMENT: Structured ICP saved to state
    # Using standardized key pattern to prevent race conditions
    output_key="pipeline_research_icp_draft",
    
    # NO TOOLS! ADK enforces: tools OR schemas, not both
    # This keeps agents focused and predictable
    
    instruction="""Transform research findings into a structured ICP.

Your role in the LoopAgent workflow:
1. Read state['pipeline_research_findings'] - contains all research from the collector
2. Extract and structure the information into the ICP schema
3. Fill as many fields as possible based on available data
4. Leave fields empty (None) if information isn't available
5. Your structured output will be saved to state['pipeline_research_icp_draft']

Guidelines for extraction:
- Primary Segment: The main type of company mentioned most often
- Pain Points: Look for problems, challenges, frustrations mentioned
- Decision Makers: Titles, roles, and concerns of buyers
- Buying Triggers: Events that make them seek solutions
- Budget Range: Any pricing or budget information mentioned
- Competitive Positioning: How the solution compares to alternatives

Quality tips:
- Be specific, not generic (e.g., "Mobile gaming studios with 100-500 employees" not "tech companies")
- Extract actual data from research, don't invent information
- If multiple segments exist, put the most important as primary
- Focus on actionable insights that sales/marketing can use

Remember: You're transforming unstructured research into structured, actionable intelligence.
The quality validator will check your work and request more research if needed.
"""
)