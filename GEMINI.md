# GEMINI.md

## Project Overview

This directory contains the materials for the **MCIT AI Agents Workshop Series**. The project is designed to teach participants how to build production-ready AI agents using the Gemini CLI and the Google Agent Development Kit (ADK).

The workshop revolves around a fictional company, **AgentFlow AI**, which is developing an AI-powered DevOps automation platform. Participants will build a series of agents that contribute to AgentFlow AI's business goals, starting with a **Market Researcher Agent**.

The main technologies used in this project are:

*   **Python 3.9+**
*   **Node.js 20**
*   **Gemini CLI**
*   **Google Agent Development Kit (ADK)**
*   **uv** (Python package manager)

## Building and Running

The primary workflow for this project involves setting up the development environment, running a verification script, and then using the Google ADK to develop and run the AI agents.

### 1. Environment Setup

The `README.md` file provides a comprehensive guide for setting up the development environment on macOS, Windows, and Linux. The setup process involves installing:

*   Python 3.9+
*   Git
*   Node.js 20 (via NVM)
*   Gemini CLI

### 2. Verification

A Python script is provided to verify that the environment is set up correctly. To run the verification script:

```bash
python3 scripts/verify_setup.py
```

### 3. Running the Agent

The AI agents are built and run using the Google ADK. The primary command to run the agent in a web-based development UI is:

```bash
adk web
```

This will start a local server, and you can interact with the agent by navigating to `http://127.0.0.1:8000` in your browser.

## Development Conventions

*   **Python Package Management:** The project uses `uv` to manage Python dependencies. The `pyproject.toml` file in each agent's directory defines the project's dependencies.
*   **Agent Structure:** Agents are developed using the Google ADK's code-first approach. The core logic for an agent is typically defined in an `agent.py` file, with prompts and instructions in a `prompt.py` file.
*   **Credentials:** Google Cloud credentials are required to use the Gemini API. These are managed through a `credentials/credentials.json` file and a `.env` file that specifies the Google Cloud project, location, and application credentials.
*   **Workshop Structure:** The workshop is divided into milestones. Each milestone has its own set of instructions and code, allowing participants to build the agents incrementally.
