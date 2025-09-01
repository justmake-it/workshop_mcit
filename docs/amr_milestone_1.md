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
# Unified Prompt for Market Researcher Agent Workshop Documentation

  I need comprehensive documentation for Workshop 2 of our AI Agents series where
  participants build a collaborative "Market Researcher" using Google Agent Development Kit
  (ADK). This workshop has two distinct milestones that progressively build capabilities.

  ## Core Philosophy
  **"AI as Teammate, Not Tool"** - Agents must seek human guidance and incorporate
  expertise. The workshop emphasizes human-in-the-loop (HITL) workflows where AI augments
  rather than replaces human decision-making.

  ## Workshop Structure
  - **Milestone 1 (45 min)**: Build a SINGLE interactive research assistant - simple and
  scoped
  - **Milestone 2 (45 min)**: Enhance with MULTIPLE sub-agents working as a team
  - **Interface**: ADK Web UI only (http://localhost:8000) - NO CLI testing
  - **Target Market**: Gaming companies (100-500 employees) with DevOps challenges
  - **Final Output**: "Alex Chen" - Head of Platform Engineering persona

  ## Required Outputs

  Please create 3 interconnected files:

  ### File 1: `amr_milestone_1_spec.md` - Technical Specification

  Structure with these sections:

  1. **Implementation Overview**
     - Overarching goal of human augmentation
     - Two-milestone approach explanation
     - Why progressive enhancement matters

  2. **Milestone 1: Single Interactive Research Assistant**
     - **Goal**: One agent that asks questions and seeks guidance
     - **Scope**: Basic search, human decisions, simple persona creation
     - **Key Feature**: Agent asks "Should I..." before every major action
     - **User Stories** (3 for Milestone 1):
       - Story 1.1: Basic conversational search
       - Story 1.2: Guided research with decisions
       - Story 1.3: Co-create simple persona
     - **Technical Details**: Single LlmAgent with ask_human tool
     - **Output**: Basic Alex persona with human input

  3. **Milestone 2: Multi-Agent Research Team**
     - **Goal**: Transform single agent into coordinated team
     - **Enhancement**: Add 3 specialist sub-agents with personalities
     - **Key Feature**: Parallel research with human as team director
     - **User Stories** (3 for Milestone 2):
       - Story 2.1: Meet your team (Sam, Jordan, Morgan)
       - Story 2.2: Coordinate parallel research
       - Story 2.3: Strategic synthesis with advisor
     - **Technical Details**: ParallelAgent, SequentialAgent patterns
     - **Output**: Enhanced Alex with multi-source validation

  4. **Implementation Code**
     - Milestone 1 code: Single agent with ask_human
     - Milestone 2 code: Team with coordinator, specialists, advisor
     - Show progression from simple to complex

  5. **ADK Web Testing Examples**
     - Milestone 1: Simple chat interactions
     - Milestone 2: Team coordination chats

  ### File 2: `amr_milestone_1_scenarios.md` - Testing Scenarios

  Structure with:

  1. **Overview**
     - Test collaboration at each milestone
     - Progressive complexity

  2. **Milestone 1 Scenarios** (3 scenarios - keep it simple)
     - Scenario 1.1: First conversation with assistant
     - Scenario 1.2: Research with guidance
     - Scenario 1.3: Basic persona creation
     - Each shows 2-3 decision points maximum

  3. **Milestone 2 Scenarios** (4 scenarios - show enhancement)
     - Scenario 2.1: Team introduction
     - Scenario 2.2: Parallel research coordination
     - Scenario 2.3: File upload integration
     - Scenario 2.4: Strategic synthesis
     - Each shows team dynamics and multiple touchpoints

  4. **Error Handling** (1 per milestone)
     - Milestone 1: Simple data scarcity
     - Milestone 2: Team disagreements

  5. **Success Metrics**
     - Milestone 1: Basic collaboration works
     - Milestone 2: Team amplifies human expertise

  ### File 3: `amr_milestone_1_implementation_guide.md` - Setup Guide

  ## Critical Implementation Details

  ### Milestone 1 (Simple & Scoped):
  - ONE agent only
  - Basic google_search + ask_human tools
  - 3-5 human decisions total
  - Simple PatternAnalysis schema
  - Basic AlexPersona output
  - No parallel execution
  - No sub-agents

  Example Milestone 1 Code:
  ```python
  # Just one simple agent
  research_assistant = Agent(
      name="research_assistant",
      model="gemini-2.0-flash",
      instruction="""You help with market research.
      Always ask: 'What should I research first?'
      After finding data ask: 'Should I dig deeper?'""",
      tools=[google_search, ask_human],
      output_schema=PatternAnalysis
  )

  Milestone 2 (Enhanced with Sub-agents):

  - MULTIPLE agents (coordinator + 3 specialists + advisor)
  - ParallelAgent for team execution
  - SequentialAgent for workflow
  - Each specialist has personality
  - 8-10 human decisions
  - File upload capability
  - Enhanced schemas

  Example Milestone 2 Structure:
  # Team of specialists
  reddit_analyst = Agent(name="Sam", ...)
  technical_expert = Agent(name="Jordan", ...)
  industry_researcher = Agent(name="Morgan", ...)

  # Parallel execution
  research_team = ParallelAgent(
      sub_agents=[reddit_analyst, technical_expert, industry_researcher]
  )

  # Full workflow
  ai_research_department = SequentialAgent(
      sub_agents=[team_coordinator, research_team, strategy_advisor]
  )

  Key Differences Between Milestones

  | Aspect    | Milestone 1     | Milestone 2           |
  |-----------|-----------------|-----------------------|
  | Agents    | 1 assistant     | 5+ team members       |
  | Execution | Sequential only | Parallel + Sequential |
  | Decisions | 3-5 simple      | 8-10 complex          |
  | Personas  | Basic Alex      | Enhanced Alex         |
  | Tools     | search + ask    | search + ask + files  |
  | Time      | 45 min          | 45 min                |

  Workshop Flow

  1. Start with Milestone 1 - prove human-AI collaboration works
  2. "Now imagine having a whole team..." transition
  3. Build Milestone 2 - experience the multiplier effect
  4. Participants feel progression from assistant to team leader

  Remember: Milestone 1 must be simple enough to build confidence, while Milestone 2 shows
  the true power of multi-agent systems. The transformation should feel like going from
  having one helpful assistant to leading an entire research department.

  This revised prompt clearly separates:
  - **Milestone 1**: Simple, single agent with basic interactions
  - **Milestone 2**: Enhanced version with multiple sub-agents working as a team

  Each milestone has its own user stories, scenarios, and technical implementation, showing
  clear progression from simple to complex.
````
