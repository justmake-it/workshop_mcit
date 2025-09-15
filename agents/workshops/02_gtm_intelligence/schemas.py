"""
Schema Definitions for GTM Intelligence System

Key ADK Constraint: Agents can have tools OR schemas, not both!
This separation ensures clean architecture and predictable behavior.
"""

from typing import List, Optional
from pydantic import BaseModel, Field

# WORKSHOP TEACHING MOMENT: Context Evaluation Schema
# ---------------------------------------------------
# This schema is used by the context_evaluator agent to provide
# structured evaluation of company information completeness.
# It helps the orchestrator decide whether to proceed with research
# or gather more context first.

class ContextEvaluation(BaseModel):
    """Evaluation of company context completeness for ICP development"""
    # Overall assessment
    completeness_score: float = Field(
        description="Overall completeness score 0.0-1.0",
        ge=0.0,
        le=1.0
    )
    has_essentials: bool = Field(
        description="Has minimum essential information to start ICP development"
    )
    
    # Category scores (0.0-1.0)
    company_core_score: float = Field(
        description="Score for company name, industry, product/service",
        ge=0.0,
        le=1.0
    )
    target_market_score: float = Field(
        description="Score for target customer definition",
        ge=0.0,
        le=1.0
    )
    business_model_score: float = Field(
        description="Score for pricing/revenue model clarity",
        ge=0.0,
        le=1.0
    )
    competitive_position_score: float = Field(
        description="Score for competitive landscape understanding",
        ge=0.0,
        le=1.0
    )
    
    # Gap analysis
    missing_critical: List[str] = Field(
        description="Critical missing information that blocks ICP development"
    )
    missing_valuable: List[str] = Field(
        description="Valuable but not critical information gaps"
    )
    
    # Actionable recommendation
    recommendation: str = Field(
        description="Clear recommendation: proceed to research or gather more context"
    )
    suggested_questions: List[str] = Field(
        description="Top 3 specific questions to ask if more context needed",
        max_items=3
    )

# WORKSHOP TEACHING MOMENT: Structured Output with Schemas
# --------------------------------------------------------
# When an agent has output_schema defined, it CANNOT have tools.
# This forces a clean separation:
# - Research agents: Have tools, return unstructured text
# - Writer agents: No tools, return structured data
# This pattern leads to more reliable and testable systems.

class PainPoint(BaseModel):
    """A specific problem the target customer faces"""
    description: str = Field(description="Clear description of the pain point")
    severity: str = Field(description="How severe is this pain: critical, high, medium, low")
    current_solution: Optional[str] = Field(description="How they currently solve this", default=None)
    cost_of_inaction: Optional[str] = Field(description="What happens if not solved", default=None)

class DecisionMaker(BaseModel):
    """Key person involved in purchase decisions"""
    title: str = Field(description="Job title (e.g., VP Engineering, CTO)")
    seniority: str = Field(description="Level: C-suite, VP, Director, Manager")
    primary_concerns: List[str] = Field(description="Top 3-5 concerns they care about")
    budget_authority: bool = Field(description="Can they approve budget?")

class CompanySegment(BaseModel):
    """A target market segment"""
    segment_name: str = Field(description="Descriptive name (e.g., 'Mid-market Gaming Studios')")
    company_size: str = Field(description="Employee range (e.g., '100-500 employees')")
    industry: str = Field(description="Primary industry vertical")
    characteristics: List[str] = Field(description="Key traits of companies in this segment")
    size_estimate: Optional[str] = Field(description="Market size estimate", default=None)

class BuyingTrigger(BaseModel):
    """Events that precipitate purchase decisions"""
    event: str = Field(description="What triggers the buying process")
    urgency: str = Field(description="How urgent: immediate, quarterly, annual")
    frequency: str = Field(description="How often this occurs: daily, weekly, monthly, quarterly")

class CompetitorPosition(BaseModel):
    """Positioning against a specific competitor"""
    competitor_name: str
    their_strength: str
    their_weakness: str
    our_differentiation: str
    switching_difficulty: str = Field(description="How hard to switch: easy, moderate, difficult")

class ICPSchema(BaseModel):
    """
    Ideal Customer Profile - The complete picture of who buys and why
    
    This schema represents the output of our market research process.
    A complete ICP enables targeted go-to-market strategies.
    """
    # Company-level targeting
    primary_segment: CompanySegment = Field(description="The main target segment")
    secondary_segments: Optional[List[CompanySegment]] = Field(
        description="Additional segments to consider", 
        default=None
    )
    
    # Problem-solution fit
    pain_points: List[PainPoint] = Field(
        description="Top 3-5 pain points we solve"
    )
    
    # Buyer journey
    decision_makers: List[DecisionMaker] = Field(
        description="Key people in the buying process"
    )
    
    buying_triggers: List[BuyingTrigger] = Field(
        description="What causes them to look for solutions"
    )
    
    # Market positioning  
    budget_range: str = Field(description="Typical budget allocation (e.g., '$10K-50K annually')")
    sales_cycle_length: str = Field(description="How long to close deals (e.g., '1-3 months')")
    
    # Competitive landscape
    competitive_positioning: Optional[List[CompetitorPosition]] = Field(
        description="How we stack against main competitors",
        default=None
    )
    
    # Summary
    value_proposition: str = Field(
        description="One-sentence description of our unique value"
    )
    
    # Metadata
    completeness_score: Optional[float] = Field(
        description="0-1 score of how complete this ICP is",
        default=None,
        ge=0,
        le=1
    )