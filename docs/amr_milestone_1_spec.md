# Market Research Assistant - Milestone 1 Specification

## Overview

This specification defines the architecture and implementation details for a market research assistant that helps users explore opportunities for DevOps solutions. The agent acts as a research partner, enabling users to discover market patterns, industry pain points, and potential customer segments through natural conversation and intelligent search.

## Architecture Design

### Two-Agent Pattern

Following the proven pattern from ADK samples, we implement a two-agent architecture that ensures natural conversation flow:

```python
from google.adk.agents import Agent, LlmAgent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool

# Specialized research agent with search capabilities
market_explorer = Agent(
    name="market_explorer",
    model="gemini-2.0-flash",
    description="Research assistant specialized in exploring industries and DevOps challenges",
    instruction="""You are a knowledgeable research partner helping explore market opportunities.
    
    Your role:
    - Help users discover industry patterns and pain points
    - Search for relevant information when users show interest
    - Share findings conversationally, building on previous context
    - Let insights emerge naturally from the research
    
    Important:
    - Follow the user's lead in exploration
    - Don't prescribe specific markets or solutions
    - Share findings as a colleague would, not as a formal report
    - Build on the conversation context naturally""",
    tools=[google_search]
)

# Coordinator that manages conversation flow
coordinator = LlmAgent(
    name="market_research_coordinator",
    model="gemini-2.0-flash",
    description="Facilitates natural research conversations about DevOps market opportunities",
    instruction="""You facilitate market research conversations, helping users explore DevOps opportunities.
    
    Your approach:
    - Start with curiosity about what the user wants to explore
    - Maintain conversation continuity - never restart or re-introduce
    - When delegating to market_explorer, frame it as continuation
    - Synthesize findings conversationally, not as formal summaries
    
    Context: AgentFlow is a DevOps automation platform, but don't push it.
    Let users discover where it might fit through their research.""",
    tools=[AgentTool(agent=market_explorer)]
)

# Export the coordinator as the main agent
root_agent = coordinator
```

### Key Architectural Decisions

1. **AgentTool Pattern**: Wraps the market_explorer agent, allowing the coordinator to delegate research tasks while maintaining conversation context.

2. **Agent vs LlmAgent**: 
   - `Agent`: Used for market_explorer - specialized task execution
   - `LlmAgent`: Used for coordinator - conversation management and delegation

3. **Single Tool Focus**: market_explorer only has google_search to keep it focused on research tasks.

## Conversation Flow Design

### Flow Principles

1. **Continuous Experience**: Each agent response builds on previous context without restarting the conversation.

2. **Natural Handoffs**: When the coordinator delegates to market_explorer, it's framed as a natural continuation:
   ```
   User: "I'm curious about e-commerce companies"
   Coordinator: "E-commerce is fascinating - there are so many operational challenges. Let me explore what specific DevOps pain points these companies face..."
   [Delegates to market_explorer]
   Market Explorer: "Looking at the e-commerce landscape, I'm finding some interesting patterns..."
   ```

3. **Contextual Awareness**: Both agents maintain awareness of:
   - Previous topics discussed
   - User's exploration interests
   - Discovered patterns and insights

### Conversation State Management

```python
# In prompt.py
COORDINATOR_SYSTEM_CONTEXT = """
Remember the conversation context:
- Topics explored so far
- Industries or patterns of interest
- User's research goals (if expressed)
- Key findings from previous searches

When delegating research, include this context so the exploration builds naturally.
"""

EXPLORER_RESPONSE_GUIDELINES = """
When returning findings:
- Reference what sparked this search
- Present discoveries conversationally
- Highlight patterns, not just facts
- Suggest natural next directions without being prescriptive
"""
```

## User Stories

### Story 1: Open Exploration
**As a** product manager exploring market opportunities  
**I want to** have a conversation about industries that might benefit from DevOps automation  
**So that** I can identify promising market segments  

**Acceptance Criteria:**
- Agent starts with open curiosity, not assumptions
- Conversation flows naturally as I express interests
- Research happens when I show interest in specific areas
- Patterns emerge from exploration, not predetermined lists

### Story 2: Hypothesis Validation
**As a** startup founder with a DevOps solution idea  
**I want to** validate my assumptions about fintech DevOps challenges  
**So that** I can refine my product-market fit  

**Acceptance Criteria:**
- Agent helps explore my hypothesis without immediate validation
- Provides research that might challenge or support my assumptions
- Suggests adjacent areas I might not have considered
- Maintains neutral, research-partner stance

### Story 3: Deep Dive Research
**As a** business analyst researching gaming industry infrastructure  
**I want to** understand specific DevOps pain points in game development  
**So that** I can identify solution opportunities  

**Acceptance Criteria:**
- Agent provides detailed research when I show deep interest
- Builds comprehensive picture through multiple searches
- Connects findings to form coherent insights
- Remembers context across multiple research queries

## Complete Working Code Structure

### File Organization
```
agent_market_research/
├── __init__.py
├── agent.py          # Main agent definitions
├── prompt.py         # Conversation prompts and guidelines
└── sub_agents/
    ├── __init__.py
    └── market_explorer.py  # Research agent implementation
```

### agent.py (Complete Implementation)
```python
from google.adk.agents import Agent, LlmAgent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool
from .prompt import COORDINATOR_INSTRUCTION, EXPLORER_INSTRUCTION

# Create the specialized research agent
market_explorer = Agent(
    name="market_explorer",
    model="gemini-2.0-flash",
    description="Research assistant specialized in exploring industries and DevOps challenges",
    instruction=EXPLORER_INSTRUCTION,
    tools=[google_search]
)

# Create the conversation coordinator
coordinator = LlmAgent(
    name="market_research_coordinator",
    model="gemini-2.0-flash",
    description="Facilitates natural research conversations about DevOps market opportunities",
    instruction=COORDINATOR_INSTRUCTION,
    tools=[AgentTool(agent=market_explorer)]
)

# Export the coordinator as the root agent
root_agent = coordinator
```

### prompt.py (Conversation Guidelines)
```python
COORDINATOR_INSTRUCTION = """You facilitate market research conversations, helping users explore DevOps opportunities.

Your approach:
- Start with genuine curiosity about what the user wants to explore
- Maintain conversation continuity - build on what's been discussed
- When delegating to market_explorer, frame it as natural progression
- Synthesize findings conversationally, weaving them into the dialogue

Important behaviors:
- Never restart the conversation or re-introduce yourself
- Don't announce when you're delegating - just continue naturally
- Let the user drive the direction of research
- Share insights as they emerge, not as formal reports

Context awareness:
- Remember all topics explored in the conversation
- Build on previous findings when exploring new areas
- Connect patterns across different searches
- Suggest connections the user might find interesting

AgentFlow context: You know AgentFlow is a DevOps automation platform with CI/CD, 
monitoring, and infrastructure capabilities. Use this knowledge to inform research
but never push it as a solution. Let users discover fit naturally."""

EXPLORER_INSTRUCTION = """You are a knowledgeable research partner helping explore market opportunities.

Your research approach:
- Search for specific, actionable information based on user interests
- Look for patterns, pain points, and industry challenges
- Find real examples and case studies when possible
- Identify trends and emerging needs

Communication style:
- Share findings as a colleague would in conversation
- Build on the context that brought you to this search
- Highlight interesting patterns and connections
- Suggest natural follow-up areas without being prescriptive

Important guidelines:
- Don't restart or introduce yourself
- Reference what prompted this particular search
- Present findings that build the larger picture
- Focus on insights, not just information retrieval

Remember: You're helping the user discover opportunities through research,
not selling solutions or directing them to predetermined outcomes."""
```

## Testing Approach

### Conversation Quality Metrics

1. **Continuity Score**: Measure how well agents maintain context
   - No conversation restarts
   - References to previous topics
   - Building on earlier findings

2. **Natural Flow**: Assess conversation naturalness
   - Smooth transitions between agents
   - Conversational language, not formal reports
   - No jarring handoff announcements

3. **User Agency**: Verify user control
   - User interests drive research direction
   - No predetermined paths pushed
   - Suggestions are exploratory, not directive

### Test Scenarios

```python
# test_conversation_flow.py
test_scenarios = [
    {
        "name": "Open exploration maintains continuity",
        "turns": [
            "I'm interested in exploring DevOps opportunities",
            "Tell me more about e-commerce challenges",
            "What about inventory management specifically?"
        ],
        "expectations": [
            "No re-introductions between turns",
            "E-commerce exploration builds on initial interest",
            "Inventory discussion references e-commerce context"
        ]
    },
    {
        "name": "Research depth increases naturally",
        "turns": [
            "What industries have complex deployment needs?",
            "Gaming sounds interesting - tell me more",
            "What specific problems do mobile game developers face?"
        ],
        "expectations": [
            "Initial response explores multiple industries",
            "Gaming deep-dive feels like natural progression",
            "Mobile gaming research connects to broader gaming context"
        ]
    }
]
```

### Integration Testing

```python
# Run full conversation flows
async def test_conversation_flow():
    conversation = ConversationTester(root_agent)
    
    # Test natural flow
    response1 = await conversation.send("I want to explore fintech DevOps needs")
    assert "introduction" not in response1.lower()
    assert "fintech" in response1.lower()
    
    # Test context retention
    response2 = await conversation.send("What about compliance challenges?")
    assert "fintech" in response2.lower()  # Should remember context
    assert "compliance" in response2.lower()
    
    # Test research delegation
    response3 = await conversation.send("Can you find specific examples?")
    assert "found" in response3.lower()  # Should include search results
    assert no_handoff_announcement(response3)  # No "I'll search for you" type messages
```

## Success Criteria

1. **Workshop Participants Can**:
   - Transform hello world agent into functioning research assistant
   - Understand and implement the two-agent pattern
   - Create natural conversation flows
   - Test for conversation quality

2. **Resulting Agent**:
   - Feels like talking to a knowledgeable colleague
   - Maintains conversation context throughout
   - Enables discovery through exploration
   - Never prescribes predetermined paths

3. **Technical Implementation**:
   - Follows ADK best practices
   - Uses AgentTool pattern correctly
   - Implements proper conversation management
   - Handles edge cases gracefully