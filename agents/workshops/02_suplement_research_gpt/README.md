# GTM Intelligence Research GPT - Architecture Plan

## Overview
A multi-agent GTM intelligence system with fact-based research capabilities, answering three fundamental questions:
1. **Who should we go after?** (Market Researcher)
2. **How do we tell the right story?** (Content Creator)
3. **How do we reach out consistently?** (Outreach Specialist)

## Architecture Design

### 1. Agent Hierarchy

```
gtm_coordinator (LlmAgent)
├── market_researcher (LlmAgent) - Sub-orchestrator
│   ├── profile_completeness_checker (LlmAgent)
│   └── research_pipeline_gpt (SequentialAgent)
│       ├── research_planner (LlmAgent)
│       ├── research_loop (LoopAgent)
│       │   ├── search_query_generator (LlmAgent)
│       │   ├── web_researcher (LlmAgent)
│       │   ├── research_evaluator (LlmAgent)
│       │   └── research_stop_checker (BaseAgent)
│       └── research_synthesizer (LlmAgent)
├── content_creator (LlmAgent) - Sub-orchestrator
│   └── research_pipeline_gpt (reused)
└── outreach_specialist (LlmAgent) - Placeholder
```

### 2. Routing Strategy

**Based on ADK documentation (https://google.github.io/adk-docs/agents/multi-agents/):**

**Q: Can sub-agents handoff directly to siblings?**
**A:** Yes. ADK allows agents to transfer control to:
- Parent agents
- Sibling agents (other sub-agents of the same parent)
- Their own sub-agents

This is handled through:
1. **LLM-driven delegation (Auto-Flow)** - Based on agent descriptions
2. **Explicit transfer** - Using EventActions with transfer_to_agent

### 3. Agent Responsibilities

#### 3.1 GTM Coordinator
- **Role**: Main conversation router
- **Routing logic**: Based on user intent, routes to appropriate specialist
- **Implementation**: LlmAgent with sub_agents list containing all specialists

#### 3.2 Market Researcher
- **Role**: Answer "Who should we go after?"
- **Process**:
  1. Build company profile through conversation
  2. Check profile completeness (pass/fail)
  3. If pass: trigger research_pipeline_gpt for ICP research
  4. If fail: ask follow-up questions from feedback
- **State management**: Stores company_profile and market_research in session

#### 3.3 Content Creator
- **Role**: Answer "How do we tell the right story?"
- **Dependencies**: Requires market_researcher output
- **Process**:
  1. Check for existing market research in session
  2. If missing, transfer to market_researcher
  3. Otherwise, trigger research_pipeline_gpt for content strategy
- **State management**: Stores content_strategy in session

#### 3.4 Outreach Specialist
- **Role**: Answer "How do we reach out consistently?"
- **Dependencies**: Requires both market research and content strategy
- **Current implementation**: Placeholder that tells industry jokes
- **Handoff logic**: Transfers to missing prerequisite agent

#### 3.5 Research Pipeline GPT
- **Role**: Reusable fact-based research component
- **Architecture**: Mimics gemini-fullstack pattern
- **Components**:
  - **research_planner**: Creates research plan
  - **research_loop**: Iterative research with LoopAgent
  - **research_synthesizer**: Compiles final report
- **Parameterization**: Accepts prompt template for different contexts

### 4. Standard Feedback Model

We use a single **Feedback** model across all evaluation scenarios:

```python
class Feedback(BaseModel):
    """Model for providing evaluation feedback."""
    
    grade: Literal["pass", "fail"] = Field(
        description="Evaluation result. 'pass' if sufficient, 'fail' if needs revision."
    )
    comment: str = Field(
        description="Detailed explanation of the evaluation."
    )
    follow_up_queries: List[str] | None = Field(
        default=None,
        description="Specific follow-up questions if grade is 'fail'. None if 'pass'."
    )
```

#### Usage
- **profile_completeness_checker**: Evaluates if company profile is complete
- **research_evaluator**: Evaluates if research quality is sufficient
- **All future evaluators**: Same simple pattern

#### Benefits
- **KISS**: Simple pass/fail with explanation
- **DRY**: One model for all evaluation needs
- **Clear**: Unambiguous next steps
- **Consistent**: Same pattern everywhere

## Implementation Phases

### Phase 1: Core Architecture Setup
1. Create gtm_coordinator with routing logic
2. Implement basic agent stubs with descriptions
3. Test routing between agents

### Phase 2: Research Pipeline GPT
1. Implement research_planner
2. Build research_loop with:
   - search_query_generator
   - web_researcher (with search tools)
   - research_evaluator
   - research_stop_checker
3. Create research_synthesizer
4. Test with sample research tasks

### Phase 3: Market Researcher
1. Port existing company profile logic
2. Implement profile_completeness_checker with standard Feedback model
3. Connect to research_pipeline_gpt
4. Test full flow with pass/fail evaluation

### Phase 4: Content Creator
1. Implement session state checking
2. Add handoff logic to market_researcher
3. Create content strategy prompts
4. Connect to research_pipeline_gpt

### Phase 5: Outreach Specialist
1. Implement prerequisite checking
2. Add routing to missing agents
3. Create placeholder functionality

### Phase 6: Integration Testing
1. Test all routing scenarios
2. Verify session state management
3. Ensure proper handoffs

## Key Design Decisions

### 1. Workflow Agents Usage
- **SequentialAgent** for research_pipeline_gpt (deterministic flow)
- **LoopAgent** for iterative research refinement
- **Source**: https://google.github.io/adk-docs/agents/workflow-agents/

### 2. State Management
- Use session.state for sharing data between agents
- Key state variables:
  - `company_profile`
  - `market_research`
  - `content_strategy`
  - `outreach_plan`

### 3. Agent Descriptions
- Critical for LLM-driven routing
- Must be clear and distinct
- Include capabilities and dependencies

### 4. Handoff Implementation
```python
# Example handoff from content_creator to market_researcher
if not invocation_context.session.state.get("market_research"):
    actions = EventActions(transfer_to_agent="market_researcher")
    event = Event(author=self.name, actions=actions)
    yield event
```

## Technical Constraints

1. **Single Parent Rule**: Each agent instance can only have one parent
2. **Transfer Scope**: Configurable on LlmAgent (parent, siblings, sub-agents)
3. **Session Continuity**: All agents in hierarchy share same InvocationContext

## Next Steps

1. Review and approve this plan
2. Create basic project structure
3. Implement Phase 1 (Core Architecture)
4. Iteratively build and test each phase

## References

- Multi-Agent Systems: https://google.github.io/adk-docs/agents/multi-agents/
- Workflow Agents: https://google.github.io/adk-docs/agents/workflow-agents/
- Sequential Agents: https://google.github.io/adk-docs/agents/workflow-agents/sequential-agents/
- Loop Agents: https://google.github.io/adk-docs/agents/workflow-agents/loop-agents/

## File Structure
```
02_supplement_research_gpt/
├── README.md (this file)
├── agent.py (main coordinator)
├── prompts.py
├── schemas.py
└── sub_agents/
    ├── __init__.py
    ├── market_researcher.py
    ├── content_creator.py
    ├── outreach_specialist.py
    ├── profile_completeness_checker.py
    └── research_pipeline/
        ├── __init__.py
        ├── pipeline.py
        ├── planner.py
        ├── researcher.py
        ├── evaluator.py
        └── synthesizer.py
```