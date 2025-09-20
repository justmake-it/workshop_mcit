from typing import AsyncGenerator

from google.adk.agents import BaseAgent, LoopAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions

from .icp_quality_eval import icp_quality_evaluator
from .icp_researcher import icp_researcher
from .icp_writer import icp_writer


class ICPStopChecker(BaseAgent):
    """Custom agent to check if ICP quality is sufficient to stop the loop"""

    def __init__(self):
        super().__init__(
            name="icp_stop_checker",
            description="Checks if ICP quality meets the threshold to stop iteration",
        )

    async def run_async_impl(
        self, invocation_context: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        """Check the evaluation results and decide whether to stop the loop"""
        evaluation = invocation_context.session.state.get("icp_evaluation", {})
        quality_score = evaluation.get("quality_score", 0)
        is_ready = evaluation.get("is_ready", False)

        # Stop if quality score is 80% or higher, or if explicitly marked as ready
        should_stop = quality_score >= 80 or is_ready

        # Create event with escalate action to stop the loop if quality is sufficient
        actions = EventActions(escalate=should_stop)
        event = Event(
            author=self.name,
            actions=actions,
        )

        yield event


# Create the loop agent that iteratively develops the ICP
icp_loop_agent = LoopAgent(
    name="icp_development_loop",
    description="Iteratively develops high-quality ICP through research, writing, and evaluation",
    sub_agents=[
        icp_researcher,  # Researches target markets and segments
        icp_writer,  # Creates structured ICP document
        icp_quality_evaluator,  # Evaluates quality and provides feedback
        ICPStopChecker(),  # Checks if quality threshold is met
    ],
    max_iterations=3,  # Maximum 3 iterations to prevent infinite loops
)