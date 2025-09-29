import pathlib
import sys

import dotenv
import pytest
from google.adk.evaluation.agent_evaluator import AgentEvaluator

pytest_plugins = ("pytest_asyncio",)

# Add the current directory to Python path to find the agent module
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))


@pytest.fixture(scope="session", autouse=True)
def load_env():
    dotenv.load_dotenv()


@pytest.mark.asyncio
async def test_all():
    """Test the agent's basic ability on a few examples."""
    await AgentEvaluator.evaluate(
        "get_to_know_me",
        str(pathlib.Path(__file__).parent / "data"),
        num_runs=3,
    )