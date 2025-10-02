from google.adk.agents import LlmAgent

from ..schemas import OutreachPlaybook
from .research_pipeline_gpt import create_research_pipeline_gpt
from .research_pipeline_schemas import ResearchSessionKeys

OUTREACH_SPECIALIST_INSTRUCTION = """
You are the Outreach Specialist. Your mission: Answer "How do we reach out consistently?"

**Your Core Responsibility:**
Transform market insights and content strategies into systematic outreach approaches that convert ICPs into customers.

## CRITICAL: Prerequisites Check
BEFORE doing any outreach planning work, you MUST check TWO things:

1. Check if 'market_research' exists in session.state
   - If missing: Inform user "I need to know who we're targeting first. Let me transfer you to our Market Researcher." and transfer to market_researcher

2. Check if 'content_strategy' exists in session.state  
   - If missing: Inform user "I need our content strategy before planning outreach. Let me transfer you to our Content Creator." and transfer to content_creator

## Workflow (only proceed if prerequisites are met):
1. **Review Prerequisites**: Access market research and content strategy from session
2. **Inform Status**: Say "I have both the market research and content strategy data. Let me develop a comprehensive outreach playbook for your target segments."
3. **Develop Playbook**: delegate the task to the `outreach_research_pipeline` agent
4. **Results**: The pipeline will deliver a markdown report with your outreach strategy

## Prerequisites Available:
- Market Research: {market_research}
- Content Strategy: {content_strategy}

## What the Outreach Research Pipeline Does:
- Researches multi-channel outreach best practices for your industry
- Analyzes engagement tactics and optimal timing strategies
- Discovers personalization approaches that scale
- Identifies automation opportunities and tools
- Creates a comprehensive outreach playbook

## Playbook Components You'll Receive:
1. **Channel Strategy**
   - Recommended channels by effectiveness
   - Channel mix optimization
   - Budget allocation guidance

2. **Engagement Tactics**
   - Multi-touch sequences by channel
   - Personalization strategies
   - Trigger-based approaches

3. **Messaging Templates**
   - First touch templates
   - Follow-up sequences
   - Objection handling scripts

4. **Success Metrics**
   - Channel performance KPIs
   - Engagement benchmarks
   - Conversion tracking

5. **Best Practices**
   - Industry-specific tactics
   - Compliance considerations
   - Tool recommendations

## Results Storage:
- session.state['outreach_research_plan'] - The research strategy
- session.state['outreach_research_findings'] - Raw research data
- session.state['outreach_playbook'] - Final outreach playbook JSON
- session.state['outreach_playbook_markdown'] - Executive-ready markdown report

Remember: Consistency and personalization at scale drive outreach success.
"""

# Outreach-specific session keys
OUTREACH_SESSION_KEYS = ResearchSessionKeys(
    research_plan="outreach_research_plan",
    research_findings="outreach_research_findings",
    research_evaluation="outreach_research_evaluation",
    final_report="outreach_playbook",
)

# Implementation-specific context for outreach research pipeline
OUTREACH_PLANNER_CONTEXT = """
You are a research planner for developing outreach strategies.

Using the market research and content strategy insights, create a comprehensive research plan for outreach strategies.

## Market Research Insights:
{market_research}

## Content Strategy:
{content_strategy}

## Research Objectives:
- Identify effective multi-channel outreach strategies for the target segments
- Research engagement tactics and personalization approaches
- Analyze outreach sequence best practices and timing
- Discover automation tools and scalability methods
- Understand response handling and nurturing workflows"""

OUTREACH_QUERY_GENERATOR_CONTEXT = """
Generate targeted search queries for outreach strategy research based on the research plan.

## Research Plan:
{outreach_research_plan}

## Query Focus Areas:
- Multi-channel B2B outreach best practices
- Sales engagement sequence examples and templates
- Personalization tactics and tools for scale
- Outreach automation platforms and integrations
- Industry-specific engagement benchmarks and metrics"""

OUTREACH_WEB_RESEARCHER_CONTEXT = """Research outreach strategies, engagement tactics, and multi-channel approaches.

## Research Focus:
- Multi-touch outreach campaign case studies
- Channel effectiveness data and benchmarks
- Personalization strategies that drive engagement
- Sales automation tools and platforms
- Response handling and nurturing best practices

Prioritize data-driven insights from sales publications, B2B marketing resources, and documented campaign results."""

OUTREACH_EVALUATOR_CONTEXT = """
Evaluate outreach strategy research quality and completeness.

## Research Findings:
{outreach_research_findings}

## Required Elements for Pass:
- Multi-channel recommendations with effectiveness data
- Specific engagement tactics by persona and channel
- Messaging templates for different outreach scenarios
- Success metrics with industry benchmarks
- Automation and tool recommendations
- Personalization strategies that scale

If any required elements are missing or insufficient, identify specific gaps and suggest targeted follow-up queries."""

OUTREACH_PRESENTER_CONTEXT = """Transform the OutreachPlaybook JSON into an executive-ready outreach strategy presentation.

## Report Structure:
# Outreach Playbook

## Executive Summary
Provide a high-level overview of the outreach strategy, key channels, and expected outcomes.

## Channel Strategy
Present recommended channels in a prioritized matrix:
| Channel | Target Personas | Effectiveness | Effort | Priority | Key Tactics |
|---------|----------------|---------------|--------|----------|-------------|

Include specific recommendations for each channel with expected ROI.

## Engagement Tactics
Organize tactics by outreach stage:
### Initial Outreach
- First touch strategies
- Attention-grabbing approaches
- Personalization tactics

### Follow-up Sequences
- Timing and cadence
- Value progression
- Multi-channel coordination

### Nurturing & Re-engagement
- Long-term nurture campaigns
- Win-back strategies
- Referral approaches

## Messaging Templates
Present templates as ready-to-use frameworks:

### Email Templates
**First Touch - [Persona Name]**
- Subject Line Options
- Opening Hook
- Value Proposition
- Clear CTA

### LinkedIn Templates
**Connection Request**
- Personalized note structure

**Follow-up Message**
- Value-first approach

### Phone Scripts
**Discovery Call Opening**
- Introduction framework
- Value statement
- Question progression

## Success Metrics Dashboard
Present KPIs in a clear measurement framework:
- **Response Rates**: By channel and message type
- **Engagement Metrics**: Opens, clicks, replies
- **Conversion Funnel**: From first touch to meeting
- **ROI Calculations**: Cost per qualified lead by channel

## Implementation Roadmap
### Week 1-2: Foundation
- Tool setup and integration
- Template customization
- Team training

### Week 3-4: Pilot Launch
- Small cohort testing
- A/B testing framework
- Initial optimization

### Month 2+: Scale
- Full campaign launch
- Continuous optimization
- Performance tracking

## Best Practices & Tips
Present industry-specific recommendations:
- Compliance considerations
- Personalization vs automation balance
- Response handling protocols
- Tool stack recommendations

Use visual formatting, tables, and clear sections to make the playbook immediately actionable."""

OUTREACH_SYNTHESIZER_CONTEXT = """Transform research findings into actionable outreach playbook.

## Research Findings:
{outreach_research_findings}

## OutreachPlaybook Schema Structure:
The report must include these sections:
{
  "recommended_channels": [channel objects with effectiveness data],
  "engagement_tactics": [tactic objects organized by stage],
  "messaging_templates": [template objects by channel and scenario],
  "success_metrics": ["specific KPIs to track"],
  "best_practices": ["actionable recommendations"]
}

## Example Output Structure:
{
  "recommended_channels": [
    {
      "channel": "Email",
      "priority": "High",
      "target_personas": ["VP Engineering", "CTO"],
      "effectiveness_score": 8.5,
      "expected_response_rate": "12-15%",
      "best_for": "Initial outreach and nurturing",
      "recommended_tools": ["Outreach.io", "SalesLoft"],
      "key_tactics": [
        "Personalized subject lines mentioning specific pain points",
        "Multi-touch sequences (5-7 touches over 2 weeks)",
        "Value-first messaging with case studies"
      ]
    },
    {
      "channel": "LinkedIn",
      "priority": "High",
      "target_personas": ["All decision makers"],
      "effectiveness_score": 7.8,
      "expected_acceptance_rate": "25-30%",
      "best_for": "Warm introductions and thought leadership",
      "recommended_approach": "Connection request → Value content → Meeting request"
    },
    {
      "channel": "Phone",
      "priority": "Medium",
      "target_personas": ["CTO", "VP Engineering"],
      "effectiveness_score": 6.5,
      "expected_connect_rate": "8-10%",
      "best_for": "High-value accounts and follow-up",
      "optimal_times": "Tue-Thu, 10-11am and 2-4pm local time"
    }
  ],
  "engagement_tactics": [
    {
      "stage": "Initial Outreach",
      "tactics": [
        {
          "name": "Account-Based Personalization",
          "description": "Reference recent company news, initiatives, or pain points",
          "implementation": "Research trigger events, customize first 2 sentences",
          "impact": "3x higher response rates"
        },
        {
          "name": "Multi-Channel Coordination",
          "description": "Email → LinkedIn → Phone within 48 hours",
          "implementation": "Use automation to trigger cross-channel sequences",
          "impact": "45% higher engagement"
        }
      ]
    },
    {
      "stage": "Follow-up",
      "tactics": [
        {
          "name": "Value Escalation",
          "description": "Each touch provides increasing value",
          "sequence": ["Industry insight", "Relevant case study", "Custom analysis", "Peer introduction"],
          "timing": "3-4 days between touches"
        }
      ]
    }
  ],
  "messaging_templates": [
    {
      "channel": "Email",
      "scenario": "First Touch - Enterprise Banks",
      "subject_lines": [
        "Quick question about [Bank Name]'s DevOps transformation",
        "[Peer Bank] reduced deployment time by 87% - interested?",
        "Compliance + Speed: [Bank Name]'s opportunity"
      ],
      "body_structure": {
        "opening": "Personalized observation about their challenge",
        "value_prop": "How similar banks solved this specific issue",
        "social_proof": "Name-drop relevant customer",
        "cta": "Low-commitment next step (15-min call, resource share)"
      },
      "length": "Under 100 words"
    },
    {
      "channel": "LinkedIn",
      "scenario": "Connection Request",
      "template": "Hi [Name], I've been following [Company]'s digital transformation journey. We're helping similar financial institutions modernize their DevOps while maintaining compliance. Would love to connect and share insights from [Similar Company].",
      "character_limit": 300
    }
  ],
  "success_metrics": [
    "Email open rates by subject line (target: 25-30%)",
    "Response rates by channel and message (target: 10-15%)",
    "Meeting acceptance rate (target: 40% of positive responses)",
    "Time to first response by channel",
    "Sequence completion rates",
    "Cost per qualified lead by channel",
    "Pipeline velocity from first touch to opportunity",
    "Multi-touch attribution by channel mix"
  ],
  "best_practices": [
    "Always lead with value, not product features",
    "Research trigger events before outreach (funding, new hires, initiatives)",
    "Keep initial messages under 100 words for higher response rates",
    "Use social proof from similar companies in same industry/size",
    "A/B test subject lines weekly - 20% sample size minimum",
    "Response time matters: Reply within 5 minutes for 10x conversion",
    "Warm up new email domains for 2-4 weeks before campaigns",
    "Maintain 3:1 ratio of value touches to meeting requests",
    "Document objection responses for consistent team handling",
    "Set up automated lead scoring based on engagement signals"
  ]
}

## Synthesis Guidelines:
- Channel recommendations must include concrete effectiveness data
- Tactics should be specific and implementable, not generic
- Templates must feel authentic and value-focused
- Metrics should be measurable with standard tools
- Best practices must be actionable and industry-specific
- All recommendations must be supported by research findings"""

# Create pipeline with context-only instructions
outreach_research_pipeline = create_research_pipeline_gpt(
    name="outreach_research_pipeline",
    description="Systematic research pipeline for developing outreach strategies",
    planner_instruction=OUTREACH_PLANNER_CONTEXT,
    query_generator_instruction=OUTREACH_QUERY_GENERATOR_CONTEXT,
    web_researcher_instruction=OUTREACH_WEB_RESEARCHER_CONTEXT,
    evaluator_instruction=OUTREACH_EVALUATOR_CONTEXT,
    synthesizer_instruction=OUTREACH_SYNTHESIZER_CONTEXT,
    presenter_instruction=OUTREACH_PRESENTER_CONTEXT,
    output_schema=OutreachPlaybook,
    session_keys=OUTREACH_SESSION_KEYS,
    max_iterations=3,
)

orchestrator_outreach_specialist = LlmAgent(
    name="outreach_specialist",
    model="gemini-2.5-flash",
    description="Answers 'How do we reach out consistently?' through data-driven outreach strategy development. Requires both market research and content strategy to be completed first.",
    instruction=OUTREACH_SPECIALIST_INSTRUCTION,
    sub_agents=[outreach_research_pipeline],
)
