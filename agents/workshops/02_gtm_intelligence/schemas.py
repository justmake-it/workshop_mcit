from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class CompanyFoundation(BaseModel):
    """Basic company information essential for understanding the business"""

    company_name: str = Field(description="Name of the company")
    core_offering: str = Field(description="What the company does in simple terms")
    industry: str = Field(description="Industry or vertical the company operates in")
    company_stage: str = Field(
        description="Stage: pre-seed, seed, series A-D, growth, enterprise"
    )
    team_size: int = Field(description="Current number of employees")
    founding_year: Optional[int] = Field(None, description="Year company was founded")


class ProductServiceCore(BaseModel):
    """Core product/service information"""

    problem_solved: str = Field(description="Main problem the product/service solves")
    key_capabilities: List[str] = Field(
        description="Top 3-5 core features or capabilities"
    )
    unique_differentiators: List[str] = Field(
        description="What makes this solution unique vs alternatives"
    )
    product_stage: str = Field(description="Product stage: idea, MVP, beta, GA, mature")


class TargetMarketReality(BaseModel):
    """Target market and customer information"""

    primary_customer_segment: str = Field(
        description="Primary target customer description"
    )
    customer_size_range: str = Field(
        description="Target company size (employees or revenue)"
    )
    target_industries: List[str] = Field(description="Industries of target customers")
    target_geography: List[str] = Field(description="Geographic markets")
    key_personas: List[str] = Field(description="Decision makers and end users")
    current_customers: Optional[int] = Field(
        None, description="Number of current customers if any"
    )


class ValuePositioning(BaseModel):
    """Value proposition and market positioning"""

    value_proposition: str = Field(description="Core value delivered to customers")
    main_alternatives: List[str] = Field(
        description="Main competitors or alternative solutions"
    )
    why_choose_us: str = Field(
        description="Primary reason customers choose this solution"
    )
    pricing_model: str = Field(description="How the product is priced")
    typical_deal_size: Optional[str] = Field(
        None, description="Average contract value or price range"
    )


class GrowthContext(BaseModel):
    """Current status and growth information"""

    revenue_status: str = Field(
        description="Current revenue status: pre-revenue, <$100k, $100k-$1M, etc"
    )
    primary_growth_channels: List[str] = Field(
        description="Main channels for customer acquisition"
    )
    biggest_growth_obstacles: List[str] = Field(
        description="Top 2-3 obstacles to growth"
    )
    twelve_month_goal: str = Field(description="Primary goal for next 12 months")
    funding_status: Optional[str] = Field(None, description="Current funding situation")


class CompanyProfile(BaseModel):
    """Complete company profile for ICP creation"""

    foundation: CompanyFoundation
    product_service: ProductServiceCore
    target_market: TargetMarketReality
    value_positioning: ValuePositioning
    growth_context: GrowthContext


class AreaScore(BaseModel):
    """Score for a specific evaluation area"""

    area_name: str
    score: int = Field(ge=0, le=100, description="Score from 0-100%")
    minimum_required: int = Field(description="Minimum score required for this area")
    is_sufficient: bool = Field(
        description="Whether the score meets minimum requirements"
    )


class EvaluationResult(BaseModel):
    """Company profile evaluation results"""

    overall_score: int = Field(
        ge=0, le=100, description="Average score across all areas"
    )
    readiness_status: str = Field(description="READY, NOT_READY, or NEEDS_MORE_INFO")

    area_scores: List[AreaScore] = Field(description="Individual scores for each area")

    missing_information: List[str] = Field(
        description="Specific information gaps identified"
    )
    follow_up_questions: List[str] = Field(
        description="Questions to ask to fill information gaps"
    )

    recommendation: str = Field(description="Clear next step recommendation")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "overall_score": 75,
                "readiness_status": "NEEDS_MORE_INFO",
                "area_scores": [
                    {
                        "area_name": "Company Foundation",
                        "score": 90,
                        "minimum_required": 80,
                        "is_sufficient": True,
                    },
                    {
                        "area_name": "Product/Service Core",
                        "score": 70,
                        "minimum_required": 70,
                        "is_sufficient": True,
                    },
                    {
                        "area_name": "Target Market Reality",
                        "score": 60,
                        "minimum_required": 70,
                        "is_sufficient": False,
                    },
                ],
                "missing_information": [
                    "Specific customer personas not defined",
                    "Pricing model unclear",
                ],
                "follow_up_questions": [
                    "Who specifically makes the buying decision?",
                    "What's your pricing structure?",
                ],
                "recommendation": "Gather more information about Target Market Reality before proceeding to ICP creation",
            }
        }
    )


class BuyerPersona(BaseModel):
    """Detailed buyer persona information"""

    title: str = Field(description="Job title or role")
    department: str = Field(description="Department they work in")
    seniority_level: str = Field(description="Seniority level: Individual Contributor, Manager, Director, VP, C-Level")
    key_responsibilities: List[str] = Field(description="Main responsibilities in their role")
    pain_points: List[str] = Field(description="Specific pain points they experience")
    goals: List[str] = Field(description="What they're trying to achieve")
    decision_criteria: List[str] = Field(description="What matters most in their buying decision")
    influence_level: str = Field(description="Decision Maker, Influencer, End User, or Champion")


class CustomerSegment(BaseModel):
    """Detailed customer segment definition"""

    segment_name: str = Field(description="Name of this customer segment")
    company_characteristics: Dict[str, str] = Field(
        description="Key company attributes (size, industry, geography, etc.)"
    )
    use_cases: List[str] = Field(description="Primary use cases for this segment")
    value_drivers: List[str] = Field(description="What drives value for this segment")
    qualifying_criteria: List[str] = Field(description="Must-have criteria to qualify")
    disqualifying_criteria: List[str] = Field(description="Factors that disqualify a prospect")
    segment_priority: str = Field(description="Priority level: Primary, Secondary, or Future")
    estimated_market_size: Optional[str] = Field(None, description="Estimated TAM for this segment")


class ICPDocument(BaseModel):
    """Structured Ideal Customer Profile document"""

    executive_summary: str = Field(description="High-level summary of the ICP")
    
    primary_segments: List[CustomerSegment] = Field(
        description="Primary customer segments to target"
    )
    secondary_segments: Optional[List[CustomerSegment]] = Field(
        None, description="Secondary segments for future expansion"
    )
    
    buyer_personas: List[BuyerPersona] = Field(
        description="Key buyer personas within target segments"
    )
    
    value_proposition_per_segment: Dict[str, str] = Field(
        description="Tailored value propositions for each segment"
    )
    
    go_to_market_recommendations: List[str] = Field(
        description="Specific GTM recommendations based on ICP"
    )
    
    anti_icp: List[str] = Field(
        description="Characteristics of customers to avoid"
    )


class ICPEvaluationResult(BaseModel):
    """ICP document quality evaluation results"""

    quality_score: int = Field(
        ge=0, le=100, description="Overall quality score from 0-100%"
    )
    
    completeness_scores: Dict[str, int] = Field(
        description="Scores for each section: segments, personas, value props, etc."
    )
    
    strengths: List[str] = Field(description="What's done well in the ICP")
    weaknesses: List[str] = Field(description="Areas needing improvement")
    
    specific_improvements: List[str] = Field(
        description="Concrete suggestions for improvement"
    )
    
    is_ready: bool = Field(
        description="Whether the ICP meets quality standards"
    )
    
    iteration_recommendation: str = Field(
        description="Specific guidance for next iteration if not ready"
    )
