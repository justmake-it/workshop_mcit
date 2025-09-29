# Workshop 3: Testing AI Agents with ADK

**Duration:** 45 minutes  
**Focus:** Essential agent testing using ADK evaluation framework

## Overview

In this workshop, we'll test the `get_to_know_me` agent using ADK's built-in evaluation tools. We'll create simple test cases and run them to verify our agent works correctly.

## Prerequisites

- Working ADK environment (verify with `adk --version`)
- Agent already created in `agent.py`
- UV package manager
- `google-adk[eval]` installed (via pyproject.toml)

## Workshop Structure

```
get_to_know_me/
├── agent.py              # Agent definition
├── prompts.py           # Agent prompts
└── eval/                # Evaluation tests
    ├── test_eval.py     # Test runner
    └── data/
        ├── conversation.test.json  # Test cases
        └── test_config.json       # Scoring thresholds
```

## Workshop Agenda

### Part 1: Test the Agent Manually (8 minutes)

First, let's see our agent in action:

```bash
# Navigate to the agent directory
cd agents/workshops/get_to_know_me
adk web .
```

Try these conversations:
1. Say "Hello"
2. Tell the agent your name
3. Ask what it wants to know about you

### Part 2: Create Evaluation Structure (10 minutes)

The evaluation structure goes inside the agent directory:

```bash
# From inside get_to_know_me directory
mkdir -p eval/data
```

### Part 3: Write Test Files (10 minutes)

We need three files for basic testing:

#### 1. Create `eval/test_eval.py`:

This file runs our tests using ADK's AgentEvaluator (create in get_to_know_me/eval/):

```python
import pathlib

import pytest
from google.adk.evaluation.agent_evaluator import AgentEvaluator

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_all():
    """Test the agent's basic ability on a few examples."""
    await AgentEvaluator.evaluate(
        "get_to_know_me",  # Module name
        str(pathlib.Path(__file__).parent / "data"),
        num_runs=3,
    )
```

**Note**: Simple and clean - no sys.path hacks or dotenv needed!

#### 2. Create `eval/data/conversation.test.json`:

These are our test cases - what we send to the agent and what we expect back (create in get_to_know_me/eval/data/):

```json
[
  {
    "query": "Hello",
    "expected_tool_use": [],
    "reference": "Hello! I'm here to get to know you better through our conversations. I'll remember what we discuss so each time we chat, I can build on what I've learned about you. What's your name?"
  },
  {
    "query": "I'm Sarah",
    "expected_tool_use": [],
    "reference": "Nice to meet you, Sarah! Where are you from?"
  },
  {
    "query": "What kind of things do you ask about?",
    "expected_tool_use": [],
    "reference": "I'd love to learn about your personal details like your location and languages, your work or studies, your hobbies and interests, and your goals. What do you do for work?"
  }
]
```

#### 3. Create `eval/data/test_config.json`:

This sets the passing thresholds for our tests (create in get_to_know_me/eval/data/):

```json
{
  "criteria": {
    "tool_trajectory_avg_score": 0.8,
    "response_match_score": 0.5
  }
}
```

**Note**: We set `response_match_score` to 0.5 because LLMs are non-deterministic and exact matches are rare.

### Part 4: Run the Tests (10 minutes)

First, ensure evaluation dependencies are installed:

```bash
# From the workshops directory
cd ..
uv sync  # This installs google-adk[eval] with all evaluation dependencies
cd get_to_know_me
```

Now let's run our evaluation:

```bash
# From inside the get_to_know_me directory
uv run pytest eval -v
```

You should see output showing:
- Test running
- Agent responses being evaluated
- Score calculations
- Pass/fail status

### Part 5: Understanding Results (5 minutes)

The evaluation checks two things:
1. **Tool Usage**: Did the agent use tools correctly? (We expect none for this simple agent)
2. **Response Match**: How similar are the agent's responses to our reference answers?

**Note**: Your tests might fail initially because the agent responds differently than expected. This is normal! LLMs are non-deterministic. For example:
- Expected: "Nice to meet you, Sarah! Where are you from?"
- Actual: "Hi Sarah! It's lovely to meet you."

Both are valid responses, but the test expects a specific one. You can:
1. Lower the threshold in `test_config.json` (already set to 0.5)
2. Update reference responses to be more generic
3. Accept that exact matching isn't always possible with LLMs

### Part 6: Add Another Test (2 minutes)

Let's add one more test case to `conversation.test.json`:

```json
{
  "query": "I'm from Toronto",
  "expected_tool_use": [],
  "reference": "Toronto is a great city! What do you do for work there?"
}
```

Run the tests again to see the new test in action.

## Key Takeaways

1. **ADK makes testing simple**: Just define inputs and expected outputs
2. **AgentEvaluator handles the complexity**: It runs your agent and compares results
3. **Tests are JSON files**: Easy to read, write, and maintain
4. **Scoring is flexible**: Adjust thresholds based on your needs

## Troubleshooting

If tests fail:
- Check if the agent module name in `test_eval.py` is `"get_to_know_me"`
- Ensure reference responses are reasonable (not exact match required)
- Lower score thresholds in `test_config.json` if needed
- Make sure you're running pytest from inside the get_to_know_me directory

## Next Steps

- Add more test cases for edge cases
- Test with different user inputs
- Integrate tests into CI/CD pipeline

## Commands Reference

```bash
# Test manually (from get_to_know_me directory)
adk web .

# Run evaluation (from get_to_know_me directory)
uv run pytest eval

# Run with verbose output
uv run pytest eval -v

# Run with immediate output
uv run pytest eval -xvs

# Run specific test
uv run pytest eval/test_eval.py::test_all
```