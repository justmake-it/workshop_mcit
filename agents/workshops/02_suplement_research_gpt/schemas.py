from typing import Dict, List, Literal, Any
from pydantic import BaseModel, Field

class Feedback(BaseModel):
    """Model for providing evaluation feedback."""
    
    grade: Literal["pass", "fail"] = Field(
        description="Evaluation result. 'pass' if sufficient, 'fail' if needs revision."
    )
    comment: str = Field(
        description="Detailed explanation of the evaluation."
    )
    follow_up_queries: List[str] | None = Field(
        default=None,
        description="Specific follow-up questions if grade is 'fail'. None if 'pass'."
    )

class CompanyProfile(BaseModel):
    """Structured company information for ICP development."""
    
    # Required fields - all must be provided for complete profile
    company_name: str
    industry: str
    company_stage: str
    team_size: str
    core_offering: str
    key_differentiators: List[str]
    current_challenges: List[str]
    
    # Optional field - helpful if provided
    additional_context: str | None = Field(
        default=None, 
        description="Any other relevant information about the company"
    )

# Domain-specific research output schemas

class MarketICPReport(BaseModel):
    """Structured report for Ideal Customer Profile research."""
    
    target_segments: List[Dict[str, Any]] = Field(
        description="Primary customer segments with demographics and size"
    )
    buyer_personas: List[Dict[str, Any]] = Field(
        description="Detailed buyer personas for each segment"
    )
    qualifying_criteria: List[str] = Field(
        description="Criteria for identifying ideal customers"
    )
    go_to_market_recommendations: List[str] = Field(
        description="Strategic recommendations for targeting segments"
    )
    market_opportunity: str = Field(
        description="Summary of market opportunity assessment"
    )


class ContentStrategyReport(BaseModel):
    """Structured report for content strategy research."""
    
    messaging_framework: Dict[str, Any] = Field(
        description="Core messaging architecture and value propositions"
    )
    content_themes: List[str] = Field(
        description="Key content themes to develop"
    )
    channel_recommendations: List[Dict[str, Any]] = Field(
        description="Recommended content channels and formats"
    )
    competitive_positioning: str = Field(
        description="How to differentiate from competitors"
    )
    content_calendar_suggestions: List[Dict[str, Any]] = Field(
        description="High-level content calendar recommendations"
    )


class OutreachPlaybook(BaseModel):
    """Structured report for outreach strategy research."""
    
    recommended_channels: List[Dict[str, Any]] = Field(
        description="Outreach channels ranked by effectiveness"
    )
    engagement_tactics: List[Dict[str, Any]] = Field(
        description="Specific tactics for each channel"
    )
    messaging_templates: List[Dict[str, Any]] = Field(
        description="Template messages for different scenarios"
    )
    success_metrics: List[str] = Field(
        description="KPIs to measure outreach effectiveness"
    )
    best_practices: List[str] = Field(
        description="Industry best practices for outreach"
    )