# Market Researcher Agent - Technical Specification

## Implementation Overview

### Overarching Goal: Human Augmentation, Not Automation

This workshop embodies the principle of "AI as Teammate, Not Tool" by building agents that actively seek human guidance and incorporate expertise at every critical decision point. Rather than creating autonomous systems that work in isolation, we design collaborative AI partners that amplify human intelligence.

### Two-Milestone Approach

The workshop uses progressive enhancement to build confidence and demonstrate the compounding value of multi-agent systems:

- **Milestone 1 (45 min)**: Participants build a single interactive research assistant that establishes the foundation of human-AI collaboration
- **Milestone 2 (45 min)**: The single agent transforms into a coordinated team, showing how multiple specialized agents can work together under human direction

### Why Progressive Enhancement Matters

1. **Learning Curve Management**: Starting simple allows participants to grasp core concepts before adding complexity
2. **Confidence Building**: Success with a basic agent motivates exploration of advanced features
3. **Real-World Alignment**: Mirrors how organizations typically adopt AI - starting with single-purpose tools before scaling to integrated systems
4. **Clear Value Demonstration**: The transformation from assistant to team dramatically illustrates the multiplier effect

---

## Milestone 1: Single Interactive Research Assistant

### Goal
Create one agent that demonstrates meaningful human-AI collaboration through constant communication and decision-seeking behavior.

### Scope
- Basic web search capabilities using `google_search` tool
- Human decision points at every major action
- Simple persona creation with human input
- No parallel execution or sub-agents
- Focus on establishing trust through transparency

### Key Feature: Proactive Question-Asking
The agent asks "Should I..." before every major action, creating natural pause points for human oversight and direction.

### User Stories

#### Story 1.1: Basic Conversational Search
**As a** workshop participant  
**I want to** have a natural conversation with my research assistant  
**So that** I understand how to guide AI agents effectively

**Acceptance Criteria:**
- Agent introduces itself and asks what to research
- Agent explains its capabilities clearly
- Agent responds to basic queries about gaming industry

#### Story 1.2: Guided Research with Decisions
**As a** workshop participant  
**I want to** guide my assistant through research decisions  
**So that** I maintain control over the research direction

**Acceptance Criteria:**
- Agent asks "What aspect should I research first?"
- After each search, agent asks "Should I dig deeper into this?"
- Agent summarizes findings and asks for next steps

#### Story 1.3: Co-create Simple Persona
**As a** workshop participant  
**I want to** work with my assistant to create a basic persona  
**So that** I see how AI can help structure insights

**Acceptance Criteria:**
- Agent asks which patterns are most relevant
- Agent proposes persona elements and seeks approval
- Final persona reflects human input and preferences

### Technical Details

#### Single LlmAgent Implementation
```python
from google.adk.agents import Agent
from google.adk.tools import google_search
from pydantic import BaseModel, Field
from typing import List, Optional
import asyncio

# Custom ask_human tool implementation
async def ask_human(question: str, context: Optional[str] = None) -> str:
    """
    Ask the human user a question and wait for their response.
    
    Args:
        question: The question to ask the human
        context: Optional context to help the human understand the question
    
    Returns:
        The human's response as a string
    """
    # In ADK Web UI, this will create an interactive prompt
    # The implementation handles the UI interaction
    if context:
        full_prompt = f"{context}\n\n{question}"
    else:
        full_prompt = question
    
    # This will pause execution and wait for human input
    # ADK Web UI will display this as an interactive element
    return full_prompt  # Placeholder - actual implementation handled by ADK

# Define simple output schema
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

# Create the single research assistant
research_assistant = Agent(
    name="research_assistant",
    model="gemini-2.0-flash",
    instruction="""You are a collaborative market research assistant helping to understand 
    gaming companies with DevOps challenges.
    
    IMPORTANT: You must seek human guidance at every major decision point:
    1. Always start by asking: "What aspect of gaming companies' DevOps challenges should I research first?"
    2. After each search, ask: "I found [brief summary]. Should I dig deeper into this aspect or explore something else?"
    3. Before creating any output, ask: "Based on my research, I'm thinking [approach]. Does this align with what you're looking for?"
    
    Be conversational and explain your thinking. You're a teammate, not a tool.""",
    description="A research assistant that collaborates with humans on market research",
    tools=[google_search, ask_human],
    output_schema=PatternAnalysis
)

# Root agent that orchestrates the research process
root_agent = Agent(
    name="market_researcher",
    model="gemini-2.0-flash",
    instruction="""You orchestrate market research about gaming companies (100-500 employees) 
    with DevOps challenges. Your goal is to create a persona for Alex Chen, Head of Platform Engineering.
    
    Work closely with the human user through your research assistant. Always prioritize human input
    and preferences. Create outputs only after getting human approval.""",
    description="Main orchestrator for market research",
    sub_agents=[research_assistant],
    output_schema=BasicAlexPersona
)
```

### Output: Basic Alex Persona
The Milestone 1 output is a simple persona containing:
- Name and role
- Company context (gaming, 100-500 employees)
- 3 main DevOps challenges (identified with human input)
- 2-3 decision factors
- All elements approved by the human user

