from pydantic import BaseModel, Field
from typing import List

class PatternAnalysis(BaseModel):
    """Analysis of patterns found in research"""
    key_patterns: List[str] = Field(description="Main patterns identified")
    supporting_evidence: List[str] = Field(description="Evidence supporting each pattern")
    confidence_level: str = Field(description="High, Medium, or Low confidence")

class BasicAlexPersona(BaseModel):
    """Basic persona for Alex Chen"""
    name: str = Field(default="Alex Chen")
    title: str = Field(default="Head of Platform Engineering")
    company_size: str = Field(description="Company size range")
    main_challenges: List[str] = Field(description="Top 3 DevOps challenges")
    decision_factors: List[str] = Field(description="What influences their decisions")