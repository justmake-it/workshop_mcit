# Market Researcher Agent

A conversational AI agent built with Google's Agent Development Kit (ADK) that helps users explore and research gaming companies and their DevOps challenges.

## Architecture

Two-agent system using AgentTool pattern:
- **Greeter Agent** - Starts natural conversations about gaming companies
- **Research Assistant** - Uses Google Search to explore topics

## Running

```bash
# From the agent directory
adk web
```

## Implementation

Uses the AgentTool pattern from ADK samples (see academic-research example) for better control and flexibility.