"""
GTM Intelligence System - Workshop 2

A company-agnostic market research system that demonstrates:
- LoopAgent for iterative refinement
- output_key for automatic state management
- include_contents for performance optimization
- EventActions(escalate=True) for loop termination

Based on ADK patterns from Financial Advisor and Gemini Fullstack samples.
"""

from .agent import root_agent

__all__ = ["root_agent"]