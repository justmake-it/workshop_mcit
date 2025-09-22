"""Reusable research pipeline with simplified configuration."""

from typing import Type

from google.adk.agents import LlmAgent, LoopAgent, SequentialAgent
from google.adk.agents.base_agent import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events.event import Event, EventActions
from google.adk.tools import google_search
from pydantic import BaseModel

from ..schemas import Feedback
from .research_pipeline_schemas import ResearchPlan, ResearchSessionKeys, SearchQueries


def build_planner_instruction(context_instruction: str) -> str:
    """
    Build complete planner instruction with ResearchPlan schema examples.
    
    Args:
        context_instruction: Implementation-specific context and objectives
        
    Returns:
        Complete instruction with schema requirements and examples
    """
    return f"""{context_instruction}

## Output Requirements
Your response must be a single, raw JSON object validating against the ResearchPlan schema.

## Schema Structure
The ResearchPlan schema requires:
- research_goals: List of specific, measurable research objectives
- search_strategies: List of strategies for finding relevant information
- success_criteria: Clear criteria for determining when research is complete

## Example Output:
{{
  "research_goals": [
    "Identify 2-3 primary customer segments with clear demographics",
    "Map decision-making process and key buyer criteria",
    "Quantify market size and growth potential for each segment"
  ],
  "search_strategies": [
    "Industry reports and market analysis from analyst firms",
    "Case studies of successful implementations in target verticals",
    "Buyer behavior research and persona studies",
    "Competitive intelligence on market positioning"
  ],
  "success_criteria": "Comprehensive profiles for 2+ segments with TAM/SAM data, 3+ validated personas per segment, clear pain points and decision criteria"
}}"""


def build_query_generator_instruction(context_instruction: str) -> str:
    """
    Build complete query generator instruction with SearchQueries schema examples.
    
    Args:
        context_instruction: Implementation-specific query generation context
        
    Returns:
        Complete instruction with schema requirements and examples
    """
    return f"""{context_instruction}

## Output Requirements
Your response must be a single, raw JSON object validating against the SearchQueries schema.

## Schema Structure
The SearchQueries schema requires:
- queries: List of search query strings to execute

## Query Generation Guidelines:
1. Create 4-6 diverse queries covering different angles
2. Mix broad market queries with specific use case queries
3. Include industry-specific terminology
4. Target different information sources (reports, case studies, forums)
5. Vary query structure to maximize coverage

## Example Output:
{{
  "queries": [
    "enterprise software adoption financial services 2024 report",
    "bank CTO decision criteria vendor selection DevOps tools",
    "fintech digital transformation case studies buyer journey",
    "financial services IT budget allocation trends Gartner",
    "DevOps platform comparison banking compliance requirements"
  ]
}}"""


def build_web_researcher_instruction(context_instruction: str) -> str:
    """
    Build complete web researcher instruction with google_search tool usage.
    
    Args:
        context_instruction: Implementation-specific research focus
        
    Returns:
        Complete instruction with tool usage patterns and examples
    """
    return f"""{context_instruction}

## Using the google_search Tool
For each query provided, you will:
1. Call google_search(query="your search query")
2. Extract relevant findings from the search results
3. Focus on credible sources (analyst reports, industry publications, case studies)
4. Synthesize information across multiple sources
5. Note source URLs for citation

## Research Process:
1. Execute each search query systematically
2. For each result, extract:
   - Key findings relevant to the research goals
   - Supporting data and statistics
   - Source credibility indicators
   - Patterns across multiple sources

## Output Format:
Compile your findings into a structured collection that includes:
- Raw findings with source attribution
- Key themes and patterns identified
- Credibility assessment of sources
- Gaps or areas needing further research

## Tool Usage Example:
When you receive queries like ["enterprise DevOps adoption 2024", "banking IT decision makers"], you would:
1. First search: google_search(query="enterprise DevOps adoption 2024")
2. Analyze results, extract relevant insights
3. Second search: google_search(query="banking IT decision makers")
4. Compile findings from both searches

Remember: Quality over quantity - focus on extracting actionable, relevant insights rather than collecting all available information."""


def build_evaluator_instruction(context_instruction: str) -> str:
    """
    Build complete evaluator instruction with Feedback schema examples.
    
    Args:
        context_instruction: Implementation-specific evaluation criteria
        
    Returns:
        Complete instruction with schema requirements and examples
    """
    return f"""{context_instruction}

## Output Requirements
Your response must be a single, raw JSON object validating against the Feedback schema.

## Schema Structure
The Feedback schema requires:
- grade: "pass" or "fail" (string literal)
- comment: Detailed explanation of the evaluation
- follow_up_queries: List of specific queries if grade is "fail", null if "pass"

## Evaluation Process:
1. Review findings against stated criteria
2. Check completeness and quality of information
3. Verify credibility of sources
4. Assess actionability of insights
5. Grade "pass" only if ALL criteria are fully met
6. If "fail", provide specific queries to address gaps

## Example Output - Pass:
{{
  "grade": "pass",
  "comment": "Research successfully identifies 3 distinct customer segments (Enterprise Banks, Regional Credit Unions, Fintech Startups) with detailed demographics, validated personas including titles and decision criteria, and market sizing from Gartner/Forrester reports. All evaluation criteria met.",
  "follow_up_queries": null
}}

## Example Output - Fail:
{{
  "grade": "fail",
  "comment": "Research identifies segments but lacks specific buyer personas with job titles and decision-making criteria. Missing competitive landscape analysis and pricing sensitivity data.",
  "follow_up_queries": [
    "VP Engineering CTO decision criteria DevOps tools enterprise banks",
    "DevOps platform pricing models financial services comparison",
    "competitive analysis DevOps automation tools banking sector 2024"
  ]
}}"""


def build_synthesizer_instruction(context_instruction: str, output_schema_name: str) -> str:
    """
    Build complete synthesizer instruction with output schema requirements.
    
    Args:
        context_instruction: Implementation-specific synthesis objectives
        output_schema_name: Name of the output schema for the response
        
    Returns:
        Complete instruction with schema requirements
    """
    return f"""{context_instruction}

## Output Requirements
Your response must be a single, raw JSON object validating against the {output_schema_name} schema."""


def build_report_presenter_instruction(context_instruction: str, json_schema_name: str) -> str:
    """
    Build instruction for converting JSON report to user-friendly markdown.
    
    Args:
        context_instruction: Implementation-specific presentation guidelines
        json_schema_name: Name of the JSON schema being converted
        
    Returns:
        Complete instruction for markdown report generation
    """
    return f"""{context_instruction}

## JSON Report Data
{{{json_schema_name.lower()}_json}}

## Output Requirements
Transform the JSON data above into a well-formatted markdown report that is:
- Easy to read and understand
- Professional and executive-ready
- Structured with clear headings and sections
- Enhanced with tables, bullet points, and formatting where appropriate

Maintain all important information from the JSON while presenting it in a user-friendly narrative format."""


def create_research_pipeline_gpt(
    name: str,
    description: str,
    planner_instruction: str,
    query_generator_instruction: str,
    web_researcher_instruction: str,
    evaluator_instruction: str,
    synthesizer_instruction: str,
    presenter_instruction: str,
    output_schema: Type[BaseModel],
    session_keys: ResearchSessionKeys = ResearchSessionKeys(),
    max_iterations: int = 3,
    worker_model: str = "gemini-2.5-flash",
    critic_model: str = "gemini-2.5-flash",
) -> SequentialAgent:
    """
    Create a research pipeline with custom instructions.

    Args:
        name: Pipeline instance name
        description: Pipeline description
        planner_instruction: Context for research planner
        query_generator_instruction: Context for query generator
        web_researcher_instruction: Context for web researcher
        evaluator_instruction: Context for evaluator
        synthesizer_instruction: Context for synthesizer
        presenter_instruction: Context for markdown report presenter
        output_schema: Pydantic model for final output
        session_keys: Session state keys configuration
        max_iterations: Max refinement iterations
        worker_model: Model for worker agents
        critic_model: Model for evaluator agent
    """

    # Create agents with provided instructions merged with schema/tool requirements
    planner = LlmAgent(
        name=f"{name}_planner",
        model=worker_model,
        description="Creates structured research plan",
        instruction=build_planner_instruction(planner_instruction),
        output_schema=ResearchPlan,
        output_key=session_keys.research_plan,
    )

    query_generator = LlmAgent(
        name=f"{name}_query_generator",
        model=worker_model,
        description="Generates search queries",
        instruction=build_query_generator_instruction(query_generator_instruction),
        output_schema=SearchQueries,
    )

    web_researcher = LlmAgent(
        name=f"{name}_web_researcher",
        model=worker_model,
        description="Executes web searches",
        instruction=build_web_researcher_instruction(web_researcher_instruction),
        tools=[google_search],
        output_key=session_keys.research_findings,
    )

    evaluator = LlmAgent(
        name=f"{name}_evaluator",
        model=critic_model,
        description="Evaluates research quality",
        instruction=build_evaluator_instruction(evaluator_instruction),
        output_schema=Feedback,
        output_key=session_keys.research_evaluation,
    )

    synthesizer = LlmAgent(
        name=f"{name}_synthesizer",
        model=worker_model,
        description="Synthesizes findings into report",
        instruction=build_synthesizer_instruction(synthesizer_instruction, output_schema.__name__),
        output_schema=output_schema,
        output_key=session_keys.final_report,
    )

    # Define stop checker as inner class that captures session_keys
    class StopChecker(BaseAgent):
        """
        Checks research evaluation result and escalates to stop loop if passed.
        
        This agent is used within a LoopAgent to control iteration based on
        the evaluation feedback grade.
        """
        
        def __init__(self):
            super().__init__(
                name=f"{name}_stop_checker",
                description="Checks research evaluation and escalates to stop loop if passed"
            )
        
        async def _run_async_impl(self, ctx: InvocationContext):
            """
            Check evaluation result and escalate if research passed.
            
            The evaluation is expected to have a 'grade' field with values
            'pass' or 'fail' based on the Feedback schema.
            """
            # Get evaluation from session state using captured session_keys
            evaluation = ctx.session.state.get(session_keys.research_evaluation, {})
            
            # Check if evaluation passed
            if evaluation.get("grade") == "pass":
                # Escalate to stop the LoopAgent
                yield Event(
                    author=self.name,
                    actions=EventActions(escalate=True)
                )
            else:
                # Continue loop - evaluation failed or not found
                fail_reason = evaluation.get("comment", "No evaluation found")
                print(f"[{self.name}] Research needs refinement: {fail_reason}")
                
                yield Event(author=self.name)
    
    # Create instance of inner class
    stop_checker = StopChecker()

    refinement_loop = LoopAgent(
        name=f"{name}_refinement_loop",
        description="Iteratively refines research",
        sub_agents=[query_generator, web_researcher, evaluator, stop_checker],
        max_iterations=max_iterations,
    )

    # Create presenter agent that reads JSON from synthesizer output
    report_presenter = LlmAgent(
        name=f"{name}_presenter",
        model=worker_model,
        description="Converts JSON report to user-friendly markdown",
        instruction=build_report_presenter_instruction(
            presenter_instruction,
            output_schema.__name__
        ).replace(
            f"{{{output_schema.__name__.lower()}_json}}",
            f"{{{session_keys.final_report}}}"
        ),
        output_key=f"{session_keys.final_report}_markdown",
    )
    
    # Return complete pipeline
    return SequentialAgent(
        name=name,
        description=description,
        sub_agents=[planner, refinement_loop, synthesizer, report_presenter],
    )
