# Workshop 2 Setup Guide

## Overview

This guide will walk you through setting up the development environment for Workshop 2 Market Researcher Agent

## Prerequisites

- **Package Manager Required**: Homebrew (macOS) or Chocolatey (Windows)
- Basic terminal/command line knowledge
- checkout at branch `workshop_market_research/milestone_1_start`

## Setup Steps

### Step 1: Verify Package Manager Installation

**macOS:**

```bash
# Check if Homebrew is installed
brew --version
```

### Step 2: Install UV Package Manager

**Check if UV is already installed:**

```bash
uv --version
```

**If UV is not installed:**

**macOS (Homebrew):**

```bash
brew install uv
```

### Step 3: Create Workshop Directory Structure

Navigate to your workshop directory and create the market_researcher folder:

```bash
mkdir agents
cd agents
mkdir market_researcher
cd market_researcher
```

### Step 4: Initialize UV Project

Initialize the UV project in the market_researcher directory:

```bash
uv init

# We don't need it
rm main.py
```

This command creates:

- `pyproject.toml` - Project metadata and dependencies
- `.python-version` - Python version specification
- `main.py` - Sample entry point
- `.gitignore` - Git ignore rules
- `README.md` - Project documentation

### Step 5: Setup Google ADK

Install the google-adk package:

```
uv add google adk
```

Notice this already create the virtual environment in the `.venv` directory, let's activate it
for our terminal session.

```
source .venv/bin/activate
```

### Step 5: Create Google ADK Agent Structure

Inside the `agents/market_researcher` directory (where you ran `uv init`), create the Google ADK agent structure:

```bash
# From inside agents/market_researcher/ directory
mkdir agent_market_research
cd agent_market_research
mkdir sub_agents

# Create core agent files
touch __init__.py agent.py prompt.py
```

```python
# Let's create our first hello world agent
from google.adk.agents import Agent

root_agent = Agent(
    name="root_agent",
    model="gemini-2.0-flash",
    description=("Agent to answer general purpose questions about life"),
    instruction=("You are helpful agent who can answer any general purpose question"),
)

```

### Step 6: Setup Google ADK Credentials (Vertex AI)

After creating your agent in Step 5, follow these steps to set up Vertex AI credentials:

#### 1. Create a `.env` file

```bash
# From inside agents/market_researcher/ directory
touch .env
```

#### 2. Add Vertex AI configuration to `.env`

```env
GOOGLE_APPLICATION_CREDENTIALS=../../credentials/credentials.json
GOOGLE_CLOUD_PROJECT=workshops-0034
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_GENAI_USE_VERTEXAI=TRUE
```

**Important**: Replace `your-project-id` with your actual Google Cloud project ID.

#### 3. Ensure credentials are in place

- Your service account credentials file (`credentials.json`) should be in the `workshop_mcit/credentials/` directory
- The service account must have the `Vertex AI User` role in your Google Cloud project

### Step 7: Test Your Agent

#### 1. Activate the virtual environment

```bash
source .venv/bin/activate
```

#### 2. Run the ADK web interface

```bash
adk web
```

#### 3. Access the web UI

Open your browser to the URL shown: `http://127.0.0.1:8000`

#### Troubleshooting

If you see authentication errors:

- Verify the `.env` file is in the `agents/market_researcher/` directory
- Check that all 4 environment variables are set correctly
- Restart the ADK server if you made changes to `.env`

### Step 8: Define agent requirements based on the initial input

````
Create implementation documentation for a workshop where
  participants build a market research assistant that helps THEM
   explore opportunities for DevOps solutions. The agent assists
   the user in discovering market patterns, NOT role-playing as
  a company representative.

  ## Critical Context
  - **Agent Purpose**: A research assistant that helps users
  explore data that will allow us to segment into relevant markets, NOT an interviewer
  - **User Relationship**: The user drives research; agents
  provide assistance and search capabilities
  - **Conversation Style**: Natural, continuous flow - like
  having a knowledgeable colleague help with research
  - **Discovery Approach**: Markets, patterns, and personas
  emerge FROM research, not predetermined. We want to know which segments or markets to prioritize

  ## What Participants Already Have
  - Working ADK setup with hello world agent at
  http://localhost:8000
  - Completed workshop prerequisites (steps 1-7 in existing
  docs)
  - Basic understanding of ADK concepts

  ## Workshop Philosophy
  "AI as Research Partner" - The agent amplifies human research
  capabilities through:
  - Intelligent search and pattern recognition
  - Contextual suggestions without prescribing paths
  - Natural conversation that maintains momentum
  - Open exploration leading to validated insights

  ## Technical Architecture Pattern
  Follow the proven pattern from https://github.com/google/adk-s
  amples/tree/main/python/agents/academic-research:
  - Use `AgentTool` for wrapping sub-agents
  - `Agent` class for specialized agents
  - `LlmAgent` for coordinators
  - Explicit conversation flow management

  ## Milestone 1: Single Research Assistant (45 min)

  ### Core Implementation
  ```python
  from google.adk.agents import Agent, LlmAgent
  from google.adk.tools import google_search
  from google.adk.tools.agent_tool import AgentTool

  # Two-agent pattern for natural conversation flow
  market_explorer = Agent(
      name="market_explorer",
      instruction="Help user explore industries with DevOps
  challenges...",
      tools=[google_search]
  )

  coordinator = LlmAgent(
      name="coordinator",
      instruction="Facilitate natural research conversation...",
      tools=[AgentTool(agent=market_explorer)]
  )

  Conversation Design Principles

  1. Opening: Friendly, curious about what user wants to explore
  2. Flow: Build on previous responses, no restart between
  agents
  3. Research: Search when user shows interest, share findings
  conversationally
  4. Output: Let patterns and personas emerge from exploration

  Required Files

  1. amr_milestone_1_spec.md

  - Architecture using AgentTool pattern (NOT SequentialAgent)
  - Conversation flow design for continuous experience
  - User stories showing research partnership (not
  interrogation)
  - Complete working code with natural handoffs
  - Testing approach for conversation quality

  2. amr_milestone_1_scenarios.md

  - User explores gaming → discovers specific pain points
  - User starts broad → narrows to fintech through research
  - User has hypothesis → agent helps validate/challenge
  - Each scenario shows natural conversation flow

  3. amr_milestone_1_implementation_guide.md

  - Transform hello world into research assistant
  - Implement conversational prompts (NO formal greetings in
  handoffs)
  - Test full conversation flows, not just individual responses
  - Success = feels like one continuous conversation

  Critical Implementation Notes

  Conversation Continuity

  # BAD - Agents restart conversation
  PROMPT = "Hello! I'm here to help with research..."

  # GOOD - Agents continue naturally
  PROMPT = "Based on your interest in [topic], let me
  explore..."

  User Agency

  # BAD - Agent assumes direction
  "Let's research gaming companies for AgentFlow"

  # GOOD - Agent follows user lead
  "What industry aspects interest you most?"

  Context Awareness

  - Agents know about AgentFlow's capabilities as context
  - They DON'T push AgentFlow or assume it's the focus
  - Context informs their assistance, doesn't drive it

  Testing Requirements

  1. Full conversation flows, not individual agent responses
  2. Different user paths (gaming, fintech, e-commerce, etc.)
  3. Conversation should feel natural and continuous
  4. User should feel in control throughout
  5. Insights should emerge, not be predetermined

  Workshop Success Metrics

  - Participants build agents that feel like research partners
  - Conversations flow naturally without jarring transitions
  - Users discover insights through exploration
  - Technical patterns from ADK samples properly implemented
  - No role-playing or interviewing behavior

  What NOT to Include

  - ADK setup instructions
  - Environment configuration
  - Theoretical explanations without code
  - Predetermined market focus or personas
  - Formal/support-ticket style interactions

  Remember

  The academic-research example shows the way: Clean
  architecture, natural conversation flow, and agents that
  amplify human capabilities. Every design decision should
  support the user's research journey, not prescribe it.
````
