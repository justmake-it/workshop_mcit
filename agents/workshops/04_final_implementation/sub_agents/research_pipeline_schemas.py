"""Generic schema definitions for the research pipeline GPT."""

from typing import Any, Dict, List

from pydantic import BaseModel, Field


class ResearchPlan(BaseModel):
    """Structured research plan output."""

    research_goals: List[str] = Field(description="Specific research goals to achieve")
    search_strategies: List[str] = Field(
        description="Strategies for finding information"
    )
    success_criteria: str = Field(
        description="Criteria for determining research completeness"
    )


class SearchQueries(BaseModel):
    """Search queries for web research."""

    queries: List[str] = Field(description="List of search queries to execute")


class ResearchFindings(BaseModel):
    """Raw research findings from web searches."""

    raw_findings: List[Dict[str, Any]] = Field(
        description="List of findings with source information"
    )
    sources: List[str] = Field(description="List of source URLs")


class ResearchSessionKeys(BaseModel):
    """Configurable session state keys for research pipeline."""

    research_plan: str = Field(
        default="research_plan", description="Key for research plan"
    )
    research_findings: str = Field(
        default="research_findings", description="Key for findings"
    )
    research_evaluation: str = Field(
        default="research_evaluation", description="Key for evaluation"
    )
    final_report: str = Field(
        default="research_report", description="Key for final report"
    )
