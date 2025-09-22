from typing import List, Literal
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

# Note: Domain-specific research output schemas (MarketICPReport, ContentStrategyReport, etc.)
# will be implemented in Phase 3+ as part of the workshop exercises