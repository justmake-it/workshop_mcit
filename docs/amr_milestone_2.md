# AMR Milestone 2: GTM Intelligence System with ADK

## Executive Summary

This milestone transforms the existing market research agent into a company-agnostic system that forms the foundation of a larger GTM (Go-To-Market) intelligence platform. The design leverages Google ADK's built-in abstractions while respecting framework constraints, particularly the separation of tool usage and structured output.

**Based on ADK Samples**: This design follows patterns from ADK's Financial Advisor (iterative context gathering) and Gemini Fullstack (research loop with validation) agents.

## 1. High-Level System Overview (The Mission)

### System Purpose

Build a **GTM Intelligence System** that transforms any company profile into actionable go-to-market strategies through three specialized agents working in concert. Each agent is designed as a **plug-and-play module** that can function independently or as part of the larger system.

### Core Architecture Principles

1. **Functional Composition**: Each agent transforms inputs into structured outputs deterministically
2. **Memory-Driven Intelligence**: Long-term learning through Vertex AI Memory Bank
3. **Iterative Refinement**: Loop agents enable continuous improvement through validation feedback (similar to ADK's Gemini Fullstack research loop)
4. **State-Driven Orchestration**: Complex workflows managed through ADK's state hierarchy

### System Components

```python
# Master Orchestrator - Routes and coordinates specialist agents
gtm_orchestrator = LlmAgent(
    name="gtm_orchestrator",
    model="gemini-2.5-pro",  # Pro model for complex orchestration
    description="Routes GTM strategy requests to appropriate specialists: market research for ICP development, content creation for messaging strategy, or outreach planning for engagement tactics",
    instruction="Coordinate GTM development using company context and past learnings. Route requests based on current context depth.",
    sub_agents=[market_researcher_pipeline, content_creator_pipeline, outreach_pipeline],
    tools=[search_memory_tool]  # Can search past GTM strategies
)

# Market Researcher Pipeline - Iterative ICP development
market_researcher_pipeline = LoopAgent(
    name="market_researcher_loop",
    description="Develops detailed ICPs through iterative research and validation. Handles both open-ended discovery from minimal context and document analysis from comprehensive profiles.",
    sub_agents=[
        research_collector,      # output_key="research_findings"
        icp_writer,             # output_key="icp_draft"
        quality_validator       # output_key="validation_result"
    ],
    max_iterations=5
)

# Content Creator Pipeline - Transform ICP into content strategy
content_creator_pipeline = SequentialAgent(
    name="content_pipeline",
    description="Transforms validated ICPs into actionable content strategies including messaging frameworks, content themes, and channel-specific recommendations based on target audience insights.",
    sub_agents=[
        content_analyzer,       # Analyzes ICP for content opportunities
        content_strategist,     # Creates structured content plan
        content_validator       # Ensures strategy aligns with ICP
    ]
)

# Outreach Pipeline - Creates personalized engagement strategies
outreach_pipeline = ParallelAgent(
    name="outreach_pipeline",
    description="Creates multi-channel outreach strategies with personalized email sequences, social media engagement plans, and event participation strategies tailored to ICP preferences.",
    sub_agents=[
        email_sequence_creator,    # output_key="outreach_email_strategy"
        social_strategy_creator,   # output_key="outreach_social_strategy"
        event_strategy_creator     # output_key="outreach_event_strategy"
    ]
)
```

### Key Design Decisions

1. **Separation of Tool Use and Structured Output**
   - Research agents use tools (search, browse) but return unstructured data
   - Writer agents take unstructured input and produce structured schemas
   - This respects ADK's constraint while maintaining flexibility

2. **Loop-Based Iterative Refinement**
   - Market researcher uses LoopAgent for iterative ICP development
   - Each iteration builds on previous findings stored in state
   - Similar to ADK's Gemini Fullstack "Iterative Research & Critique Loop"

3. **Memory-Driven Learning**
   - Every completed ICP is stored in Vertex AI Memory Bank
   - Future research can search past ICPs for similar companies
   - System learns patterns across multiple engagements

4. **State Management Strategy**
   ```python
   # State hierarchy usage:
   "app:industry_templates"     # Shared ICP templates
   "user:company_profile"       # User's company details
   "current_icp_draft"         # Session-specific ICP work
   "temp:search_results"       # Temporary research data
   ```

## 2. User and Cross-Agent Collaboration Scenarios (The Vision)

### Scenario 1: Progressive Context Building from Minimal Input

```
User: "I'm building a DevOps automation platform"

GTM Orchestrator checks memory and state:
  → Searches memory: No previous conversations found
  → Checks user:company_profile: Empty
  → Creates session state: conversation_stage = "discovery"

Research Collector: "I'll help you develop an ideal customer profile. Let me understand 
your platform better. What specific DevOps challenge does it solve?"

User: "It prevents pipeline failures"

Research Collector updates state:
  → session.state["product_focus"] = "pipeline failure prevention"
  → session.state["temp:research_topics"] = ["CI/CD failures", "deployment risks"]
  → Searches: "CI/CD pipeline failure statistics 2024"

Research Collector: "Interesting! Pipeline failures cost companies millions. How does 
your solution prevent them - is it monitoring, testing, or something else?"

User: "We use AI to predict failures before they happen"

State updates:
  → session.state["technology"] = "AI/ML predictive analytics"
  → user:company_profile["core_capability"] = "AI-powered failure prediction"
  
Research Collector: "Predictive DevOps is cutting edge! Who do you envision using this?
Any specific industry or company size in mind?"

User: "Gaming companies during launches"

[Multiple state updates and research queries...]

After 15-20 conversational turns:
  → user:company_profile gradually populated with ~30 data points
  → session.state contains current ICP draft
  → Memory service stores conversation for future reference

Quality Validator: "We now have enough context to create your ICP. However, I'm missing:
- Your pricing model
- Competitive differentiation
- Technical requirements
Would you like to continue building the profile or proceed with what we have?"
```

### Scenario 2: Resuming with Existing Context

```
User: "Let's continue working on my ICP"

GTM Orchestrator checks context:
  → Searches memory: Finds 3 previous sessions for this user
  → Loads user:company_profile: Contains 30+ data points from past conversations
  → Retrieves last session state: ICP 70% complete

Research Collector: "Welcome back! I see we were developing an ICP for your AI-powered 
DevOps platform targeting gaming studios. Last time we identified:
- Primary segment: Mobile gaming studios (100-500 employees)
- Key pain point: Launch day failures costing $100K+ per hour
- Your differentiation: 73% failure prediction accuracy

We still need to define:
1. Decision maker profiles
2. Budget allocation patterns
3. Buying triggers

Shall we continue from where we left off?"

User: "Actually, we've pivoted slightly. We're now focusing on e-commerce too"

State updates:
  → session.state["pivot_flag"] = true
  → session.state["new_segments"] = ["e-commerce"]
  → Memory search: "e-commerce DevOps challenges Black Friday"

Research Collector: "Interesting pivot! E-commerce has similar high-stakes deployment 
windows. Let me research how their DevOps challenges compare to gaming..."

[Continues building on existing context while incorporating new direction]
```

### Scenario 3: Processing Comprehensive Company Profile Document

```
User: [Provides 200+ line company profile document similar to AgentFlow AI profile]

GTM Orchestrator analyzes document:
  → Detects structured company information
  → Plans extraction strategy

Research Collector: "I've received your comprehensive company profile. Let me process 
this systematically..."

Document processing and state updates:
  → user:company_profile = {
      "name": "AgentFlow AI",
      "industry": "DevOps/Observability", 
      "stage": "pre-seed",
      "funding": "30K",
      "team_size": 2,
      // ... 50+ extracted fields
    }
  → session.state["profile_completeness"] = "high"
  → session.state["validation_needed"] = ["market_claims", "competitor_comparison"]

Research Collector: "I've extracted the key information. Your profile shows you're 
targeting gaming studios with a prevention-first approach. Let me validate some claims:
- You mention 73% prediction accuracy - how was this measured?
- You claim 80% cost savings vs Datadog - is this TCO or subscription only?
- Gaming focus is clear, but what makes gaming studios special for your solution?"

User: "The 73% is from our beta tests with 5 studios..."

[Research validates claims and enriches profile with market data]

Memory storage:
  → Complete profile stored in user:company_profile 
  → Validated ICP stored in memory for future reference
  → Industry insights cached in app:gaming_devops_insights
```

### Scenario 4: Memory-Augmented ICP Development

```
User: "We're a DevOps platform targeting financial services"

GTM Orchestrator with memory search:
  → Searches: "DevOps platform financial services ICP"
  → Finds: 5 similar companies' ICPs in memory
  
Research Collector: "I found several similar platforms that successfully targeted 
financial services. Based on their experiences:

Common patterns identified:
- Primary buyers: VP of Engineering, CISO (dual approval needed)
- Key pain points: Compliance automation, audit trails
- Budget cycles: Annual, requires security review
- Deal size: $100-500K ACV

One platform similar to yours pivoted from gaming to fintech and found:
- Longer sales cycles (3-6 months vs 1-2 months)
- Higher ACVs but fewer deals
- Compliance features became critical

Should we use these insights as a starting point for your ICP?"

User: "Yes, but we're more focused on smaller banks"

[Adapts learned patterns to specific context]
```

### Scenario 5: Cross-Agent Intelligence with State Management

```
Content Creator needs ICP context:

Content Creator queries state:
  → Reads session.state["icp_final"] 
  → Checks user:company_profile["competitive_advantages"]
  → Searches memory: "gaming DevOps content performance"

State-based insights discovered:
  → app:industry_insights["gaming_cto_priorities"] = ["speed", "reliability", "cost"]
  → user:past_content["best_performing"] = "launch day war stories"
  
Content Creator: "Based on the ICP and past performance data, I recommend:
1. Lead with speed - '10-minute setup' resonates with gaming CTOs
2. Use launch day scenarios - 73% higher engagement
3. Avoid deep technical specs - they care about outcomes"

Outreach Specialist reads accumulated state:
  → All ICP data from market researcher
  → Content themes from content creator
  → Timing insights from app:gaming_industry_calendar

Creates coordinated outreach plan using full context.
```

### Scenario 6: Handling Partial Context and Ambiguity

```
User: "We need an ICP"

Research Collector checks context:
  → user:company_profile: Empty
  → Memory search: No previous conversations
  
Research Collector: "I'll help you create an ICP. First, I need to understand your 
business. Could you tell me:
- Your company/product name?
- What you do in one sentence?"

User: "We do AI stuff for developers"

Research Collector: "That's a start! 'AI for developers' covers many areas. To create 
a meaningful ICP, I need more specifics:

Are you:
□ Code generation/assistance (like GitHub Copilot)?
□ Testing/QA automation?
□ DevOps/deployment optimization?
□ Documentation/knowledge management?
□ Something else?

What made you start this company?"

User: "My deploys kept failing at my last job"

State updates:
  → session.state["founder_pain_point"] = "deployment failures"
  → session.state["temp:hypothesis"] = "DevOps/deployment focus"
  
Research Collector: "Ah, personal experience with deployment pain! That's powerful. 
Tell me more about those failures - what was causing them?"

[Gradually builds context through empathetic conversation]
```

### Scenario 7: Thinking-Enhanced ICP Development

```
User: "We're building an AI platform for developers but struggling to find our niche"

GTM Orchestrator (with thinking_budget=-1):
  [THINKING: User has vague direction. Need to:
   1. Understand what kind of AI platform
   2. Identify developer pain points they solve
   3. Check memory for similar platforms
   Let me search memory first, then route to researcher.]
  
  → Memory search: "AI platform developers ICP"
  → Finds 3 similar cases with different niches

GTM Orchestrator: "I found insights from similar AI platforms. Let me help you 
discover your unique position. Starting with market research..."

Research Collector (with thinking_budget=256):
  [THINKING: "AI for developers" is too broad. Priority questions:
   1. What specific developer workflow? (coding, testing, deployment?)
   2. What makes it AI-powered?
   3. Personal motivation - usually reveals true differentiator]
  
Research Collector: "AI for developers is a competitive space. To find your niche,
let's start with your personal experience. What specific developer problem 
frustrated you enough to build this?"

User: "I kept shipping bugs because I couldn't test edge cases properly"

Research Collector:
  [THINKING: Testing/QA focus. Edge case problem. Need to understand:
   - Current testing approach
   - Why edge cases are hard
   - How AI helps]
  
  → Searches: "AI testing edge cases developer tools 2024"
  → Updates state with testing/QA focus

Research Collector: "Edge case testing is a $2B problem! How does your AI 
approach it differently than existing tools like Cypress or Playwright?"

[Continues with focused, intelligent questioning...]

Quality Validator (with thinking_budget=128):
  [THINKING: ICP has good problem definition but missing:
   - Company size sweet spot (startups vs enterprise)
   - Pricing model alignment
   - Integration requirements
   Priority: company size - determines everything else]

Quality Validator: "Your ICP is shaping up well. The critical missing piece:
What size development teams have both the edge case problem AND budget for
AI solutions? This will determine your entire go-to-market approach."
```

**Key Thinking Enhancements Demonstrated:**
1. **Orchestrator**: Uses memory insights to guide conversation
2. **Research Collector**: Prioritizes questions based on reasoning
3. **Quality Validator**: Identifies most critical gap through thinking
4. **Efficiency**: Each agent thinks at appropriate depth for their task

## 3. Market Researcher Detailed Implementation Plan

### Phase 1: Core Architecture (1 hour)

#### 1.1 Agent Definitions

```python
# Research Collector - Has tools, returns unstructured data
research_collector = LlmAgent(
    name="research_collector",
    model="gemini-2.5-flash",
    description="Conducts market research through conversational discovery and web searches. Specializes in identifying industry pain points, market sizing, and competitive landscapes.",
    tools=[google_search],
    include_contents='default',  # Needs full conversation history
    output_key="research_findings",  # Automatically saves to state
    instruction="""You gather market intelligence through conversation and research.
    
    Approach:
    - Start with open-ended discovery questions
    - Use search to validate and expand on user inputs
    - Focus on: industry, company size, pain points, budget, decision makers
    - Your output will be automatically saved to state['research_findings']
    """
)

# ICP Writer - No tools, structured output
icp_writer = LlmAgent(
    name="icp_writer",
    model="gemini-2.5-flash",
    description="Transforms unstructured market research into structured Ideal Customer Profiles with segments, pain points, decision makers, and buying triggers.",
    output_schema=ICPSchema,
    include_contents='none',  # Stateless transformation - faster processing
    output_key="icp_draft",  # Structured ICP saved to state
    instruction="""Transform research findings into structured ICP.
    
    Read state['research_findings'] and create comprehensive ICP.
    Ensure all sections are data-driven and specific.
    Your structured output will be saved to state['icp_draft'].
    """
)

# Quality Validator - Validates and guides
quality_validator = LlmAgent(
    name="quality_validator",
    model="gemini-2.5-flash",
    description="Validates ICP completeness and identifies critical missing information. Provides specific questions to guide next research iteration.",
    include_contents='none',  # Only needs ICP data from state
    output_key="validation_result",  # Validation feedback to state
    instruction="""Validate ICP completeness and accuracy.
    
    Read state['icp_draft'] and check for:
    - All required fields populated with specific data
    - Internal consistency
    - Actionable insights
    
    If incomplete, specify what's missing for research_collector.
    If complete, set validation_result['is_complete'] = True.
    Your output will be saved to state['validation_result'].
    
    IMPORTANT: When ICP is complete, also generate an event with escalate=True
    to properly terminate the LoopAgent:
    Event(content="ICP validation complete", actions=EventActions(escalate=True))
    """
)
```

**Key Design Benefits:**
- **Automatic State Management**: `output_key` eliminates manual state updates
- **Performance Optimization**: `include_contents='none'` for stateless agents
- **Clear Data Contracts**: Each agent's output has a defined state location
- **Testing Friendly**: Can test agents in isolation with mock state

#### 1.2 Schema Design

The ICP schema includes:
- **Company Segments**: Primary and secondary target segments
- **Decision Makers**: Titles, seniority, concerns, budget authority
- **Pain Points**: Description, severity, current solutions, cost of inaction
- **Buying Triggers**: Events that precipitate purchase decisions
- **Competitive Positioning**: Differentiation against key competitors

#### 1.3 ADK Feature Utilization

**Understanding `output_key` - Automatic State Management**

The `output_key` parameter is fundamental to our LoopAgent architecture:

```python
# Data flow through the loop via output_keys
Loop Iteration 1:
  research_collector → state["research_findings"] = "Initial market research..."
  icp_writer → state["icp_draft"] = {structured ICP attempt 1}
  quality_validator → state["validation_result"] = {"is_complete": false, "missing": [...]}

Loop Iteration 2:
  research_collector reads state["validation_result"]["missing"]
  research_collector → state["research_findings"] = "Enhanced research with gaps filled..."
  icp_writer → state["icp_draft"] = {improved ICP attempt 2}
  quality_validator → state["validation_result"] = {"is_complete": true}
```

**Understanding `include_contents` - Context Optimization**

This parameter controls how much conversation history each agent receives:

| Agent | include_contents | Rationale |
|-------|-----------------|-----------|
| research_collector | 'default' | Needs conversation history to ask follow-up questions |
| icp_writer | 'none' | Pure transformation task - only needs state data |
| quality_validator | 'none' | Validation is stateless - only needs ICP to validate |

**Performance Benefits:**
- Agents with `include_contents='none'` process 2-3x faster
- Reduced token usage and API costs
- Cleaner agent logic - each agent has single responsibility
- Easier debugging - can inspect exact inputs/outputs

**State Flow Pattern:**
```python
# The LoopAgent automatically manages this flow
market_researcher_pipeline = LoopAgent(
    name="market_researcher_loop",
    sub_agents=[
        research_collector,  # output_key="research_findings"
        icp_writer,         # output_key="icp_draft"  
        quality_validator   # output_key="validation_result"
    ],
    max_iterations=5
)

# Each iteration builds on previous outputs automatically
# No manual state management needed!
```

#### 1.4 Enhanced Reasoning with Native Thinking

**Leveraging Gemini 2.5's Native Thinking Capabilities**

Both Gemini 2.5 Flash and Pro models include native thinking capabilities, allowing agents to reason through problems before responding. We use `BuiltInPlanner` with `ThinkingConfig` to enhance our agents' reasoning abilities.

```python
from google.adk.agents import LlmAgent
from google.adk.agents.planners import BuiltInPlanner
from google.adk.types import ThinkingConfig

# GTM Orchestrator - Complex reasoning with Pro model
gtm_orchestrator = LlmAgent(
    name="gtm_orchestrator",
    model="gemini-2.5-pro",  # Pro for complex orchestration
    planner=BuiltInPlanner(
        thinking_config=ThinkingConfig(
            include_thoughts=True,    # Transparent reasoning for debugging
            thinking_budget=-1        # Automatic budget based on complexity
        )
    ),
    description="GTM strategy orchestrator with transparent reasoning",
    instruction="""Think through the best approach before routing to specialists.
    Consider: user context depth, available memory, and optimal agent sequence.
    
    Use transfer_to_agent for dynamic routing:
    - If user has no company context → transfer_to_agent(agent_name='market_researcher_loop')
    - If ICP exists but no content strategy → transfer_to_agent(agent_name='content_pipeline')
    - If content exists but no outreach → transfer_to_agent(agent_name='outreach_pipeline')
    
    You can receive transfers back from specialists when they need guidance or escalate issues.""",
    sub_agents=[market_researcher_pipeline, content_creator_pipeline, outreach_pipeline],
    tools=[search_memory_tool],
    disallow_transfer_to_parent=False,  # Can escalate if needed
    disallow_transfer_to_peers=False    # Can transfer to sibling agents
)

# Research Collector - Strategic thinking for research
research_collector = LlmAgent(
    name="research_collector",
    model="gemini-2.5-flash",
    planner=BuiltInPlanner(
        thinking_config=ThinkingConfig(
            include_thoughts=False,   # Internal reasoning only
            thinking_budget=256       # Limited budget for efficiency
        )
    ),
    include_contents='default',
    output_key="research_findings",
    tools=[google_search],
    instruction="""Think about the most important questions to ask based on context.
    Prioritize questions that will fill critical ICP gaps."""
)

# ICP Writer - No planner needed
icp_writer = LlmAgent(
    name="icp_writer",
    model="gemini-2.5-flash",
    # No planner - pure transformation task doesn't benefit from thinking
    output_schema=ICPSchema,
    include_contents='none',
    output_key="icp_draft",
    instruction="Transform research findings into structured ICP."
)

# Quality Validator - Reasoning for validation priorities
quality_validator = LlmAgent(
    name="quality_validator",
    model="gemini-2.5-flash",
    planner=BuiltInPlanner(
        thinking_config=ThinkingConfig(
            include_thoughts=False,
            thinking_budget=128      # Minimal budget for validation logic
        )
    ),
    include_contents='none',
    output_key="validation_result",
    instruction="""Think through validation priorities. Focus on the most critical
    missing elements that would make the ICP actionable."""
)
```

**Thinking Budget Best Practices:**

| Setting | Use Case | Behavior |
|---------|----------|----------|
| `thinking_budget=0` | Disable thinking | No reasoning process |
| `thinking_budget=-1` | Automatic (recommended) | Model decides based on complexity |
| `thinking_budget=128-256` | Simple tasks | Quick reasoning for straightforward logic |
| `thinking_budget=512+` | Complex tasks | Deep reasoning for multi-step planning |

**Key Benefits of Native Thinking:**
1. **Improved Question Sequencing**: Research collector prioritizes questions intelligently
2. **Better Orchestration**: GTM orchestrator makes smarter routing decisions
3. **Focused Validation**: Validator identifies most critical gaps first
4. **Cost Control**: Explicit budgets prevent excessive token usage
5. **Debugging**: `include_thoughts=True` reveals agent reasoning process

**Important Configuration Note:**
```python
# CORRECT: ThinkingConfig must be in BuiltInPlanner
planner=BuiltInPlanner(
    thinking_config=ThinkingConfig(...)
)

# INCORRECT: Will raise an error!
generate_content_config=GenerateContentConfig(
    thinking_config=ThinkingConfig(...)  # Not allowed here
)
```

#### 1.5 State Key Conventions and Standardization

**Preventing Race Conditions and Ensuring Scalability**

To avoid state conflicts and enable scalable multi-agent systems, we use standardized state key naming conventions:

```python
# State Key Naming Conventions
STATE_KEY_PATTERNS = {
    # Pipeline outputs - primary results from each pipeline
    "research": {
        "findings": "pipeline_research_findings",
        "icp": "pipeline_research_icp_final",
        "validation": "pipeline_research_validation"
    },
    
    # Content pipeline outputs
    "content": {
        "analysis": "pipeline_content_analysis",
        "strategy": "pipeline_content_strategy",
        "validation": "pipeline_content_validation"
    },
    
    # Outreach pipeline - distinct keys for parallel execution
    "outreach": {
        "email": "parallel_outreach_email_strategy",
        "social": "parallel_outreach_social_strategy",
        "event": "parallel_outreach_event_strategy",
        "combined": "pipeline_outreach_combined"  # Aggregated result
    },
    
    # Cross-agent communication
    "transfer": {
        "request": "transfer_{from_agent}_to_{to_agent}_request",
        "context": "transfer_{from_agent}_to_{to_agent}_context"
    },
    
    # Loop iteration tracking
    "loop": {
        "iteration": "loop_{agent_name}_current_iteration",
        "history": "loop_{agent_name}_iteration_history"
    }
}

# Example usage in parallel agents to prevent race conditions
email_sequence_creator = LlmAgent(
    name="email_sequence_creator",
    output_key="parallel_outreach_email_strategy",  # Unique key
    description="Creates personalized email sequences based on ICP insights"
)

social_strategy_creator = LlmAgent(
    name="social_strategy_creator",
    output_key="parallel_outreach_social_strategy",  # Unique key
    description="Develops social media engagement strategies for target segments"
)

event_strategy_creator = LlmAgent(
    name="event_strategy_creator",
    output_key="parallel_outreach_event_strategy",  # Unique key
    description="Plans event participation and networking strategies"
)
```

**Benefits of Standardized Keys:**
1. **No Race Conditions**: Parallel agents write to distinct keys
2. **Clear Data Lineage**: Easy to trace data flow through pipelines
3. **Debugging**: Predictable state structure in ADK Web
4. **Extensibility**: New agents follow established patterns
5. **Testing**: Mock specific state keys for unit tests

### Phase 2: Context & Conversation Management (1 hour)

#### 2.1 Iterative Context Building Strategy

**Context Accumulation Pattern**:
The Research Collector builds context incrementally through the LoopAgent's iterations, following the pattern from ADK's Financial Advisor which asks for ticker → risk attitude → investment period. Each iteration:
1. Reads the validator's feedback on what's missing
2. Asks targeted questions to fill gaps
3. Searches for supporting information
4. Outputs findings via `output_key`

**Conversation Modes**:
1. **Cold Start**: No prior context, gradual discovery
2. **Warm Start**: Some user/company data exists
3. **Document Import**: Rich context from file
4. **Resumption**: Continuing previous work

#### 2.2 State Management Architecture

```python
# State hierarchy for market researcher
STATE_SCHEMA = {
    # App-level: Shared across all users
    "app:industry_templates": {},          # Reusable ICP templates
    "app:industry_insights": {},           # Accumulated market knowledge
    "app:competitor_data": {},             # Competitor intelligence
    
    # User-level: Persists across sessions
    "user:company_profile": {              # Gradually built company data
        "name": str,
        "industry": str,
        "stage": str,
        "product": {},
        "team": {},
        "financials": {},
        # ... 50+ fields
    },
    "user:past_icps": [],                  # Historical ICP versions
    "user:preferences": {},                # User's interaction preferences
    
    # Session-level: Current conversation
    "icp_draft": {},                       # Working ICP document
    "conversation_stage": str,             # discovery|refinement|validation
    "profile_completeness": float,         # 0.0 to 1.0
    "validation_status": {},               # What's been verified
    
    # Temporary: Current invocation only
    "temp:search_results": [],             # Current search data
    "temp:extraction_buffer": {},          # Document parsing workspace
}
```

#### 2.3 Context-Aware Question Generation

The Research Collector adapts questions based on what the Quality Validator identifies as missing:

```python
# Example instruction for Research Collector
instruction="""You gather market intelligence through conversation and research.

Approach:
- Read state['validation_result']['missing'] to see what information is needed
- Ask specific questions to fill those gaps
- Use search to validate and expand on user inputs
- Focus on: industry, company size, pain points, budget, decision makers
"""
```

### Phase 3: Memory Integration (1 hour)

#### 3.1 Memory Storage Patterns

```python
# Store completed ICP with rich metadata
async def store_icp_in_memory(ctx: InvocationContext):
    icp_data = ctx.state.get("icp_draft")
    company_profile = ctx.state.get("user:company_profile")
    
    memory_entry = {
        "type": "completed_icp",
        "timestamp": datetime.now().isoformat(),
        "metadata": {
            "company_name": company_profile["name"],
            "industry": company_profile["industry"],
            "company_stage": company_profile["stage"],
            "target_segments": icp_data["segments"],
            "iteration_count": ctx.state.get("loop_iterations"),
            "conversation_turns": len(ctx.session.events),
            "profile_completeness": ctx.state.get("profile_completeness")
        },
        "icp_data": icp_data,
        "company_profile": company_profile,
        "conversation_insights": extract_key_insights(ctx.session)
    }
    
    # Store in memory service
    await ctx.memory_service.add_session_to_memory(ctx.session)
    
    # Also update app-level learnings
    update_industry_insights(ctx, icp_data)
```

#### 3.2 Memory-Augmented Research Patterns

```python
# Search and apply past learnings
class MemoryAugmentedResearcher:
    async def enhance_research_with_memory(self, ctx: InvocationContext, query: str):
        # 1. Search for similar companies
        similar_companies = await ctx.memory_service.search_memory(
            app_name=ctx.app_name,
            user_id=ctx.session.user_id,
            query=f"ICP {query} industry:{ctx.state['user:company_profile']['industry']}"
        )
        
        # 2. Extract patterns from successful ICPs
        patterns = self.extract_icp_patterns(similar_companies)
        
        # 3. Search for industry-specific insights
        industry_insights = await ctx.memory_service.search_memory(
            app_name=ctx.app_name,
            user_id="*",  # Search across all users
            query=f"insights {ctx.state['user:company_profile']['industry']}"
        )
        
        # 4. Apply learnings to current research
        return {
            "similar_icps": patterns,
            "industry_insights": industry_insights,
            "suggested_approach": self.generate_approach(patterns, industry_insights)
        }
```

#### 3.3 Conversation Resumption via Memory

```python
# Resume incomplete ICP development
async def resume_icp_development(ctx: InvocationContext):
    # Check for incomplete work
    if "user:partial_icp" in ctx.state:
        partial_icp = ctx.state["user:partial_icp"]
        last_stage = partial_icp.get("last_stage", "unknown")
        
        return f"""Welcome back! I see we were working on your ICP and got to the 
        {last_stage} stage. We had identified:
        - Target: {partial_icp.get('primary_segment', 'Not yet defined')}
        - Key insight: {partial_icp.get('key_insight', 'Still exploring')}
        
        Would you like to continue from where we left off, or start fresh with new insights?"""
    
    # Search memory for any past attempts
    past_attempts = await ctx.memory_service.search_memory(
        app_name=ctx.app_name,
        user_id=ctx.session.user_id,
        query="ICP development incomplete"
    )
    
    if past_attempts:
        return "I found previous ICP work. Would you like me to summarize what we learned?"
```

### Phase 4: Testing Strategy (1 hour)

#### 4.1 Test Scenarios

1. **AgentFlow AI Test**: Full company profile provided
2. **Generic Input Test**: "We're a B2B SaaS company"
3. **Pivot Test**: Company changing target market
4. **Memory Test**: Similar company research acceleration
5. **Handoff Test**: State passing to content creator

#### 4.2 Success Criteria

- Handles vague inputs gracefully
- Produces complete, actionable ICPs
- Leverages memory effectively
- Maintains conversation context
- Enables smooth agent handoffs

## 4. Implementation Considerations

### Loop Agent Orchestration

The LoopAgent manages iterative ICP refinement through a pattern similar to ADK's Gemini Fullstack agent, which uses a critic model to evaluate findings and refine questions:

```python
# Loop control with context awareness
class ICPDevelopmentLoop(LoopAgent):
    def __init__(self):
        super().__init__(
            name="icp_development_loop",
            sub_agents=[research_collector, icp_writer, quality_validator],
            max_iterations=5
        )
    
    async def should_continue(self, ctx: InvocationContext) -> bool:
        # Check validation result
        validation = ctx.state.get("validation_result", {})
        if validation.get("is_complete"):
            return False
            
        # Check iteration count
        if self.current_iteration >= self.max_iterations:
            # Save partial work after max iterations
            ctx.state["user:partial_icp"] = ctx.state.get("icp_draft")
            return False
            
        # Check user fatigue
        if ctx.state.get("user_requested_pause"):
            ctx.state["user:partial_icp"] = ctx.state.get("icp_draft")
            return False
            
        return True
```

### Context Building Through Agent Collaboration

**Explicit Data Flow via output_keys:**

```python
# Iteration 1 - Cold Start
Research Collector (include_contents='default'):
  INPUT: User conversation + empty state
  PROCESS: Asks discovery questions, gathers initial info
  OUTPUT via output_key: state["research_findings"] = {
    "company_type": "DevOps platform",
    "problem_area": "pipeline failures",
    "initial_research": "CI/CD failure statistics..."
  }

ICP Writer (include_contents='none'):
  INPUT: state["research_findings"] only
  PROCESS: Transforms unstructured data to structured ICP
  OUTPUT via output_key: state["icp_draft"] = {
    "segments": [{"segment_name": "Gaming Studios", "size_estimate": "Unknown"}],
    "pain_points": [{"description": "Pipeline failures", "severity": "Unknown"}],
    // ... incomplete fields
  }

Quality Validator (include_contents='none'):
  INPUT: state["icp_draft"] only  
  PROCESS: Validates completeness
  OUTPUT via output_key: state["validation_result"] = {
    "is_complete": false,
    "missing": ["company_size", "budget_range", "decision_makers"],
    "next_questions": ["What size gaming studios can afford your solution?"]
  }

# Iteration 2 - Targeted Refinement
Research Collector:
  INPUT: Previous conversation + state["validation_result"]["next_questions"]
  PROCESS: Asks specific questions from validator, enriches profile
  OUTPUT via output_key: state["research_findings"] = {
    // Previous data plus:
    "company_size": "100-500 employees",
    "budget_insights": "Gaming studios allocate $50K-200K for DevOps",
    "enhanced_research": "Mobile gaming studio infrastructure..."
  }

[Data flows automatically through agents via output_keys]
```

**Key Benefits of This Architecture:**
1. **No Manual State Management**: ADK handles all state updates
2. **Performance**: ICP Writer and Validator skip conversation processing
3. **Debugging**: Can inspect state at each step in ADK Web
4. **Testing**: Can mock specific state keys for unit tests
5. **Scalability**: Easy to add new agents to the pipeline

### ADK Web Interface Configuration

Configure the system using ADK's built-in web interface:

1. **Agent Composition**:
   - Drag-and-drop agent creation
   - Visual loop configuration
   - State schema definition

2. **Memory Configuration**:
   ```yaml
   memory_service: vertexai://project-id/us-central1/memory-bank-id
   session_service: vertexai://project-id/us-central1
   ```

3. **State Inspection**:
   - Real-time state visualization
   - Debug conversation flow
   - Track context accumulation

### State Flow Architecture

The use of `output_key` and `include_contents` creates a clean, functional data pipeline:

```python
# Complete data flow through market researcher pipeline
def market_researcher_data_flow():
    """
    Iteration N State Evolution:
    
    PRE: state = {
        "user:company_profile": {...},  # Persistent profile
        "research_findings": "Previous research...",
        "icp_draft": {previous ICP},
        "validation_result": {"is_complete": false, "missing": [...]}
    }
    
    RESEARCH COLLECTOR:
      - Reads: state["validation_result"]["missing"]
      - Uses: include_contents='default' (sees conversation)
      - Writes: state["research_findings"] (via output_key)
    
    ICP WRITER:
      - Reads: state["research_findings"]
      - Uses: include_contents='none' (stateless transform)
      - Writes: state["icp_draft"] (via output_key)
    
    QUALITY VALIDATOR:
      - Reads: state["icp_draft"]
      - Uses: include_contents='none' (stateless validation)
      - Writes: state["validation_result"] (via output_key)
    
    POST: state = {
        ...updated with new values from each agent
    }
    """
```

**Integration Benefits:**
1. **ADK Web Visualization**: Each output_key appears as inspectable state
2. **Testing**: Can inject test data at any state key
3. **Debugging**: Clear data lineage through the pipeline
4. **Performance Monitoring**: Track processing time per agent

### Production Deployment

Using Vertex AI services for:
- **SessionService**: Persistent conversation state with automatic scaling
- **MemoryService**: Semantic search across all ICPs and insights
- **Deployment**: Vertex AI Agent Engine with built-in monitoring

### Workshop Execution Plan

**Hour 1**: System architecture and context/memory concepts
**Hour 2**: Progressive context building scenarios  
**Hour 3**: Loop agent configuration in ADK Web
**Hour 4**: Testing with various context depths

## 5. Future Extensions

While this milestone focuses on the market researcher, the architecture enables:

1. **Content Creator Integration**: Uses ICP to generate content strategies
2. **Outreach Specialist**: Creates multi-channel engagement plans
3. **Analytics Agent**: Tracks ICP accuracy and refinement needs
4. **Industry Specialist Agents**: Deep expertise for specific verticals

Each extension follows the same principles:
- Clear input/output contracts
- Memory-driven intelligence
- Human-in-the-loop refinement
- State-based coordination

## 6. Scalability Patterns and Best Practices

### Hub-and-Spoke Pattern for Industry Specialization

As the system grows, add industry-specific specialists as spokes:

```python
# Future extension: Industry-specific market researchers
gaming_specialist = LlmAgent(
    name="gaming_market_specialist",
    description="Deep expertise in gaming industry DevOps challenges, launch patterns, and buying behaviors",
    tools=[gaming_industry_search_tool],
    output_key="gaming_insights"
)

fintech_specialist = LlmAgent(
    name="fintech_market_specialist",
    description="Specializes in financial services compliance, security requirements, and procurement processes",
    tools=[fintech_regulation_tool],
    output_key="fintech_insights"
)

# Orchestrator routes to specialists based on industry
gtm_orchestrator.sub_agents.extend([gaming_specialist, fintech_specialist])
```

### Pipeline Extension Pattern

Easy addition of new pipeline stages:

```python
# Analytics Pipeline - Future extension
analytics_pipeline = SequentialAgent(
    name="analytics_pipeline",
    description="Tracks ICP accuracy, content performance, and outreach effectiveness to suggest strategy refinements",
    sub_agents=[
        performance_tracker,      # Monitors KPIs
        insight_generator,       # Identifies patterns
        refinement_suggester     # Proposes improvements
    ]
)

# Feedback Loop Integration
feedback_loop = LoopAgent(
    name="continuous_improvement",
    sub_agents=[
        analytics_pipeline,
        market_researcher_pipeline  # Re-runs with insights
    ],
    max_iterations=3
)
```

### Memory-Driven Learning at Scale

```python
# Industry-specific memory banks
memory_config = {
    "gaming": "vertexai://project/us-central1/gaming-memory-bank",
    "fintech": "vertexai://project/us-central1/fintech-memory-bank",
    "ecommerce": "vertexai://project/us-central1/ecommerce-memory-bank"
}

# Dynamic memory selection based on context
async def get_industry_memory(ctx: InvocationContext):
    industry = ctx.state.get("user:company_profile", {}).get("industry")
    return memory_config.get(industry, "vertexai://project/us-central1/general-memory")
```

### Best Practices for Production

1. **Agent Naming Conventions**:
   ```python
   # Pattern: {function}_{specialization}_{type}
   "market_researcher_gaming_specialist"
   "content_creator_b2b_strategist"
   "outreach_email_sequencer"
   ```

2. **Error Handling and Resilience**:
   ```python
   # Add retry logic for critical agents
   resilient_researcher = LlmAgent(
       name="resilient_researcher",
       retry_config=RetryConfig(max_attempts=3, backoff_factor=2),
       fallback_behavior="use_cached_results"
   )
   ```

3. **Performance Monitoring**:
   ```python
   # Track agent performance metrics
   AGENT_METRICS = {
       "research_time": "avg_seconds_per_iteration",
       "icp_quality": "validation_pass_rate",
       "memory_hits": "cache_hit_ratio"
   }
   ```

4. **Version Control for Prompts**:
   ```python
   # Maintain prompt versions for A/B testing
   PROMPT_VERSIONS = {
       "research_collector_v1": "original_prompt",
       "research_collector_v2": "enhanced_with_examples",
       "research_collector_v3": "industry_specific_variants"
   }
   ```

### Anti-Patterns to Avoid

1. **❌ Overlapping State Keys**: Always use unique, prefixed keys
2. **❌ Unbounded Loops**: Always set max_iterations
3. **❌ Silent Failures**: Implement explicit error handling
4. **❌ Monolithic Agents**: Keep agents focused on single responsibilities
5. **❌ Ignoring Transfer Capabilities**: Use LLM-driven routing for flexibility

## Key Innovations in Context Management

This design addresses the challenge of building rich context from minimal input through:

### 1. Iterative Context Accumulation
- Starts with single-line input ("I'm building a DevOps platform")
- Each LoopAgent iteration adds more context based on validation feedback
- Uses state hierarchy to persist partial work across sessions
- Enables resumption at any stage of development

### 2. Memory-Driven Intelligence
- Every conversation contributes to long-term learning
- Similar companies' ICPs accelerate new development
- Industry insights accumulate at app level
- Semantic search enables intelligent pattern matching

### 3. Adaptive Conversation Flow
- Questions evolve based on validator feedback
- Handles vague inputs with empathetic exploration
- Validates claims through targeted research
- Supports both discovery and document import modes

### 4. State Management Excellence
```
app:     Shared learnings across all users
user:    Company profile persists across sessions  
session: Current ICP work and progress
temp:    Transient research data
```

## Conclusion

This design creates a sophisticated, company-agnostic market researcher that truly leverages ADK's context and memory capabilities:

- **Context-Aware**: Builds from minimal to comprehensive understanding
- **Memory-Augmented**: Learns from every interaction
- **Resumable**: Partial work never lost
- **Intelligent**: Questions adapt to context depth
- **Scalable**: From single-line input to full company profiles

The progressive context building approach ensures that whether a user provides a comprehensive 200-line profile or just "I build AI stuff," the system can guide them to a complete, actionable ICP through intelligent conversation and memory-driven insights.

This foundation enables the larger GTM intelligence system where context flows seamlessly between specialized agents, each building on the accumulated knowledge to deliver increasingly sophisticated go-to-market strategies.