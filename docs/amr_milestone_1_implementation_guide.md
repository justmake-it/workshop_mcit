# Market Research Assistant - Implementation Guide

## Overview

This guide walks you through transforming your hello world agent into a sophisticated market research assistant. You'll implement a two-agent architecture that enables natural conversation flow while helping users explore DevOps market opportunities.

**Time Required**: 45 minutes  
**Prerequisites**: Completed workshop setup (Steps 1-7), working hello world agent at http://localhost:8000

## Step 1: Create the Prompt Module (5 minutes)

First, we'll define the conversational instructions that make our agents feel natural.

### Create `prompt.py`

Navigate to your agent directory:
```bash
cd agents/market_researcher/agent_market_research
```

Create the prompt file:
```bash
touch prompt.py
```

Add the conversation instructions:
```python
# prompt.py

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

## Step 2: Update the Main Agent File (10 minutes)

Now we'll replace the hello world agent with our two-agent architecture.

### Backup and Update `agent.py`

First, let's backup the original:
```bash
cp agent.py agent_hello_world.py
```

Now replace the contents of `agent.py`:
```python
# agent.py

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

### Key Architecture Points

1. **Two-Agent Pattern**: 
   - `market_explorer`: Handles research with google_search
   - `coordinator`: Manages conversation flow

2. **AgentTool Wrapper**: Enables natural delegation between agents

3. **LlmAgent vs Agent**: LlmAgent for coordination, Agent for specialized tasks

## Step 3: Test Basic Functionality (5 minutes)

Let's ensure our agent loads correctly.

### Restart the ADK Server

```bash
# Stop the current server (Ctrl+C)
# Start it again
adk web
```

### Verify in Browser

1. Open http://localhost:8000
2. You should see "market_research_coordinator" as the active agent
3. Try a simple prompt: "Hello, I'm interested in exploring DevOps opportunities"

Expected behavior:
- Natural, conversational response
- No formal introduction
- Shows curiosity about your interests

## Step 4: Test Research Capabilities (10 minutes)

Now let's verify the research functionality works correctly.

### Test Progressive Depth

Try this conversation sequence:

1. **Broad Interest**:
   ```
   "I'm curious about DevOps challenges in fast-growing industries"
   ```
   - Should provide overview without immediately searching
   - Might suggest areas to explore

2. **Specific Interest**:
   ```
   "Tell me more about e-commerce infrastructure challenges"
   ```
   - Should trigger research via market_explorer
   - Results presented conversationally

3. **Deeper Dive**:
   ```
   "What specific problems do they face during Black Friday?"
   ```
   - Builds on previous context
   - More detailed research

### Verify Natural Handoffs

Watch for these success indicators:
- ✅ No "I'll search for you" announcements
- ✅ No "Hello, I'm here to help" restarts
- ✅ Smooth continuation of conversation
- ✅ Research results woven into dialogue

## Step 5: Implement Conversation Continuity Testing (10 minutes)

Create a test script to verify conversation quality.

### Create `test_conversation.py`

```python
# test_conversation.py

"""
Simple conversation flow tester for market research agent.
Run this to verify natural conversation flow.
"""

def test_conversation_flow():
    """
    Manual test script - copy/paste these prompts to verify flow
    """
    
    test_sequence = [
        {
            "prompt": "I'm exploring opportunities in financial services DevOps",
            "expect": [
                "No formal greeting or introduction",
                "Shows interest in financial services",
                "Might mention different segments (banks, fintech, etc.)",
                "Invites further exploration"
            ]
        },
        {
            "prompt": "Fintech companies seem interesting - what are their main challenges?",
            "expect": [
                "Remembers financial services context",
                "Triggers research on fintech specifically",
                "Presents findings conversationally",
                "No restart or re-introduction"
            ]
        },
        {
            "prompt": "How do they handle compliance while scaling quickly?",
            "expect": [
                "Builds on fintech context",
                "Searches for compliance + scaling information",
                "Connects to previous findings",
                "Suggests related areas naturally"
            ]
        }
    ]
    
    print("CONVERSATION FLOW TEST GUIDE")
    print("=" * 50)
    
    for i, test in enumerate(test_sequence, 1):
        print(f"\nTurn {i}:")
        print(f"SEND: {test['prompt']}")
        print("\nEXPECT:")
        for expectation in test['expect']:
            print(f"  - {expectation}")
    
    print("\n" + "=" * 50)
    print("Run these prompts in order and verify expectations")

if __name__ == "__main__":
    test_conversation_flow()
```

Run the test guide:
```bash
python test_conversation.py
```

## Step 6: Common Implementation Pitfalls (5 minutes)

### Avoiding Conversation Breaks

❌ **BAD - Agent restarts conversation**:
```python
instruction="Hello! I'm your market research assistant. How can I help you explore DevOps opportunities today?"
```

✅ **GOOD - Agent continues naturally**:
```python
instruction=EXPLORER_INSTRUCTION  # From prompt.py
```

### Ensuring Natural Delegation

❌ **BAD - Announces handoff**:
```python
"Let me search for that information for you..."
"I'll ask my research colleague to look into this..."
```

✅ **GOOD - Seamless continuation**:
```python
"E-commerce infrastructure faces fascinating challenges, especially during peak events..."
[Research happens transparently]
```

### Maintaining Context

❌ **BAD - Forgets previous context**:
```
User: "Tell me about fintech"
Agent: [Discusses fintech]
User: "What about compliance?"
Agent: "Compliance in which industry?"  # Lost context!
```

✅ **GOOD - Builds on context**:
```
User: "Tell me about fintech"
Agent: [Discusses fintech]
User: "What about compliance?"
Agent: "Fintech compliance is particularly interesting because..."  # Maintains context
```

## Step 7: Full Conversation Testing (10 minutes)

Test the complete scenarios from the documentation.

### Gaming Industry Test

1. Start fresh conversation
2. Use prompts from Scenario 1 in `amr_milestone_1_scenarios.md`
3. Verify:
   - Natural flow between research queries
   - Pattern emergence from findings
   - No prescribed solutions

### Hypothesis Validation Test

1. Start with a specific hypothesis
2. Watch how agent explores and validates
3. Verify:
   - Doesn't immediately confirm/deny
   - Uses research to build understanding
   - Helps discover nuances

## Step 8: Success Criteria Checklist

Before considering implementation complete:

### Conversation Quality
- [ ] No conversation restarts between agents
- [ ] Natural handoffs without announcements
- [ ] Context maintained throughout session
- [ ] Research triggered by user interest, not proactively

### Technical Implementation
- [ ] Two-agent architecture working correctly
- [ ] AgentTool pattern properly implemented
- [ ] Google search integration functioning
- [ ] Prompts imported from prompt.py

### User Experience
- [ ] Feels like talking to a knowledgeable colleague
- [ ] User controls research direction
- [ ] Insights emerge from exploration
- [ ] No pushing of predetermined solutions

## Advanced: Debugging Tips

### If Agents Restart Conversation

Check your prompts for introduction language:
```python
# Search for phrases like:
- "Hello"
- "I'm here to"
- "How can I help"
- "Welcome"
```

### If Handoffs Are Jarring

Ensure coordinator instruction includes:
```python
"Don't announce when you're delegating - just continue naturally"
```

### If Context Is Lost

Verify both agents reference conversation history:
```python
"Build on the context that brought you to this search"
"Remember all topics explored in the conversation"
```

## Next Steps

Once your implementation passes all tests:

1. Try the agent with real research scenarios
2. Experiment with different industries
3. Note patterns in user interactions
4. Consider enhancements for Milestone 2

Remember: The goal is a natural research partnership, not a scripted interaction. Your implementation succeeds when users forget they're talking to an AI and feel like they're exploring with a knowledgeable colleague.