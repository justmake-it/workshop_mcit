"""
GTM Intelligence System - Main Orchestration

This is the complete system that demonstrates:
1. LoopAgent for iterative ICP refinement
2. State-driven agent communication
3. Native thinking capabilities with BuiltInPlanner
4. Future extensibility for content and outreach

Based on real ADK patterns from Financial Advisor and Gemini Fullstack samples.
"""

from google.adk.agents import LlmAgent, LoopAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types
from google.adk.tools.agent_tool import AgentTool

from .prompts import GTM_ORCHESTRATOR_INSTRUCTION
from .sub_agents import icp_writer, quality_validator, research_collector, context_evaluator

# WORKSHOP TEACHING MOMENT: LoopAgent Pattern
# -------------------------------------------
# This is the heart of our iterative refinement system!
#
# LoopAgent executes sub_agents in sequence, repeatedly:
# 1. Research Collector → gathers information
# 2. ICP Writer → structures it
# 3. Quality Validator → checks completeness
#
# The loop continues until:
# - Quality Validator emits EventActions(escalate=True), OR
# - max_iterations is reached
#
# Data flows automatically through output_keys with standardized naming:
# pipeline_research_findings → pipeline_research_icp_draft → pipeline_research_validation
# This prevents race conditions and ensures clean data lineage

market_researcher_loop = LoopAgent(
    name="market_researcher_loop",
    description=(
        "Develops detailed ICPs through iterative research and validation. "
        "Handles both open-ended discovery from minimal context and document "
        "analysis from comprehensive profiles."
    ),
    sub_agents=[
        research_collector,  # output_key="pipeline_research_findings"
        icp_writer,  # output_key="pipeline_research_icp_draft", include_contents='none'
        quality_validator,  # output_key="pipeline_research_validation", can escalate=True
    ],
    max_iterations=15,  # Safety limit - prevents infinite loops
)

# WORKSHOP TEACHING MOMENT: Orchestrator Pattern with Native Thinking
# --------------------------------------------------------------------
# The orchestrator is our router that directs requests to specialists.
# It uses native thinking capabilities to:
# 1. Reason about the best approach before routing
# 2. Determine optimal agent sequence
# 3. Maintain context within the session
#
# Key features:
# - BuiltInPlanner: Enables native thinking
# - thinking_budget=-1: Automatic budget based on complexity
# - include_thoughts=True: Transparent reasoning for debugging
#
# In production, this would route to:
# - market_researcher_loop (what we built)
# - content_creator_pipeline (future)
# - outreach_specialist_pipeline (future)

gtm_orchestrator = LlmAgent(
    name="gtm_orchestrator",
    model="gemini-2.5-pro",  # Pro model for complex orchestration
    # Native thinking for intelligent routing
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,  # Transparent reasoning for debugging
            thinking_budget=-1,  # Automatic budget based on complexity
        )
    ),
    description=(
        "GTM strategy orchestrator with transparent reasoning. "
        "Routes requests to appropriate specialists based on context analysis "
        "and maintains state within the session for iterative improvement."
    ),
    instruction=GTM_ORCHESTRATOR_INSTRUCTION,
    
    # WORKSHOP TEACHING MOMENT: Agent as Tool
    # Context evaluator helps decide if we have enough info before routing
    tools=[AgentTool(agent=context_evaluator)],
    
    # Specialists
    sub_agents=[market_researcher_loop],  # Add more pipelines as built
    # Transfer configuration
    disallow_transfer_to_parent=False,  # Can escalate if needed
    disallow_transfer_to_peers=False,  # Can transfer between specialists
)

# Export the orchestrator as the root agent
root_agent = gtm_orchestrator

# WORKSHOP EXTENSION IDEAS:
# ------------------------
# 1. Add industry-specific researchers:
#    gaming_researcher = LoopAgent(...)
#    fintech_researcher = LoopAgent(...)
#
# 2. Add downstream pipelines:
#    content_creator_pipeline = SequentialAgent(...)
#    outreach_pipeline = ParallelAgent(...)
#
# 3. Add feedback loops:
#    performance_tracker = LlmAgent(...)
#    strategy_refiner = LoopAgent(...)
