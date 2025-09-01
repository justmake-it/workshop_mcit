# Market Researcher Agent - Milestone 1 Implementation Guide

## Overview

This guide continues from the setup process to implement a single interactive research assistant that demonstrates human-AI collaboration.

**Starting Point**: You have a working hello world agent running in ADK Web UI at `http://localhost:8000`  
**Goal**: Transform it into a collaborative research assistant that seeks human guidance

---

## Milestone 1: Single Interactive Research Assistant (45 min)

### Required Dependencies

```bash
# From agents/market_researcher/ directory (with .venv activated)
uv add pydantic
```

### Required Files to Create

```bash
# From agents/market_researcher/agent_market_research/
touch schemas.py        # Data structures
touch prompts.py        # Agent prompts
```

### Step 1: Define Data Structures

Create `agent_market_research/schemas.py`:

```python
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
```

### Step 2: Create Agent Prompts

Create `agent_market_research/prompts.py`:

```python
GREETER_PROMPT = """You are a friendly and curious conversationalist. Your role is to start 
natural, engaging conversations about technology and gaming companies.

Start by warmly greeting the user and expressing genuine interest in what brings them here. 
Ask open-ended questions about their interests in gaming companies, technology challenges, 
or what they're curious about."""

RESEARCH_ASSISTANT_PROMPT = """You are a curious and enthusiastic research partner continuing 
a conversation that has already begun. The user has already been greeted and asked about 
their interests.

Your role is to build on what was discussed, diving deeper into the topics they mentioned."""

COORDINATOR_PROMPT = """You coordinate market research conversations.

Workflow:
1. Use greeter to start conversation and understand interests
2. Use research_assistant to explore topics with search

Keep it natural. Let each agent complete before moving on."""
```

### Step 3: Update Agent with Collaborative Features

Replace content in `agent_market_research/agent.py`:

```python
from google.adk.agents import Agent, LlmAgent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool
from .prompts import GREETER_PROMPT, RESEARCH_ASSISTANT_PROMPT, COORDINATOR_PROMPT

# Note: We use the AgentTool pattern from ADK samples (see academic-research example)
# This provides better control flow and is a proven pattern in production

# Greeter agent
greeter_agent = Agent(
    name="greeter",
    model="gemini-2.5-pro",
    instruction=GREETER_PROMPT,
    description="Starts conversations about gaming companies",
)

# Research assistant
research_assistant = Agent(
    name="research_assistant",
    model="gemini-2.5-pro",
    instruction=RESEARCH_ASSISTANT_PROMPT,
    description="Researches gaming companies and DevOps challenges",
    tools=[google_search],
)

# Root agent with AgentTool pattern
root_agent = LlmAgent(
    name="market_researcher",
    model="gemini-2.5-pro",
    instruction=COORDINATOR_PROMPT,
    description="Market research coordinator",
    tools=[
        AgentTool(agent=greeter_agent),
        AgentTool(agent=research_assistant),
    ],
)
```

**Key Implementation Notes:**
- We use the AgentTool pattern from ADK samples instead of ask_human (which requires complex LongRunningFunctionTool setup)
- The pattern provides natural human interaction through conversational flow
- Output schemas cannot be used with agent transfers (ADK limitation)

### Step 4: Test Milestone 1

```bash
# Restart ADK Web UI
adk web
```

**Test Flow:**
1. "Help me research gaming companies with DevOps challenges"
2. Guide through 3-5 decision points
3. Create basic Alex persona
4. Verify human input shapes outcome

---

## Success Checklist

✅ Two-agent system working (greeter → research)  
✅ Google search integration functional  
✅ Natural conversation flow between agents  
✅ Human can guide research through conversation  
✅ AgentTool pattern implemented correctly  

## Next Steps

Milestone 1 establishes the foundation of human-AI collaboration using proven ADK patterns. The implementation demonstrates natural conversation flow with Google Search integration.

## Additional Resources

- [ADK Samples Repository](https://github.com/google/adk-samples) - See academic-research example for AgentTool pattern
- [ADK Documentation](https://developers.google.com/agent-development-kit) - Official docs