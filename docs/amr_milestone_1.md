# Workshop 2 Setup Guide

## Overview

This guide will walk you through setting up the development environment for Workshop 2 Market Researcher Agent

## Prerequisites

- **Package Manager Required**: Homebrew (macOS) or Chocolatey (Windows)
- Basic terminal/command line knowledge

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
