from google.adk.agents import SequentialAgent

from .company_profile_context_analyzer import company_profile_context_analyzer
from .company_profile_checker import company_profile_checker
from .company_profile_updater import company_profile_updater

company_profile_pipeline = SequentialAgent(
    name="profile_builder_pipeline",
    description="Analyzes conversation, extracts company profile, and checks completeness",
    sub_agents=[
        company_profile_context_analyzer,  # Analyzes conversation → session.state['company_profile_distilled_context']
        company_profile_updater,  # Extracts from distilled notes → session.state['company_profile']
        company_profile_checker,  # Evaluates profile → session.state['company_profile_evaluation']
    ],
)