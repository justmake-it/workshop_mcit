# GTM Intelligence v2 - Phase 2: Core Architecture & Reusable Components

## Overview

This directory represents **Phase 2** of the GTM Intelligence system implementation. At this stage, we have:

- ✅ Core architecture with main orchestrator
- ✅ Reusable research pipeline (templated)
- ✅ Company profile pipeline 
- 🔲 Full agent implementations (only stubs)

## What's Implemented

### 1. Main Orchestrator (`agent.py`)
The `gtm_coordinator` that routes conversations to specialized agents:
- Market Researcher
- Content Creator  
- Outreach Specialist

### 2. Reusable Research Pipeline (`research_pipeline_gpt.py`)
A templated, reusable research pipeline that can be configured for different research contexts:
- Research planning
- Iterative web research with quality evaluation
- Result synthesis and presentation

Key features:
- **Templated instructions** - Customize for different domains
- **SequentialAgent** pattern for deterministic flow
- **LoopAgent** for iterative refinement
- **Configurable output schemas**

### 3. Company Profile Pipeline
A complete pipeline for extracting and validating company profiles:
- Context analyzer
- Profile extractor
- Completeness checker with Feedback model

### 4. Agent Stubs
Basic implementations of the three sub-orchestrators:
- `orchestrator_market_researcher` - Basic routing only
- `orchestrator_content_creator` - Basic routing only
- `orchestrator_outreach_specialist` - Tells jokes (placeholder)

## Workshop Learning Objectives

This Phase 2 state is designed to teach:

1. **Multi-Agent Architecture**
   - How agents route and delegate
   - Parent-child agent relationships
   - Agent descriptions for LLM-driven routing

2. **Reusable Components**
   - Template pattern for research pipelines
   - Configurable prompts and schemas
   - DRY principle in agent design

3. **Workflow Agents**
   - SequentialAgent for ordered execution
   - LoopAgent for iterative processes
   - Custom BaseAgent implementations

4. **State Management**
   - Session state sharing between agents
   - Structured data flow with Pydantic schemas

## Next Steps (Phase 3+)

Workshop participants will:
1. Implement full Market Researcher using the research pipeline
2. Implement full Content Creator reusing the same pipeline
3. Add proper handoff logic and user experience flows
4. Test the complete system end-to-end

## File Structure

```
03_gtm_intelligence_v2/
├── agent.py                    # Main orchestrator
├── prompts.py                  # Orchestrator prompts
├── schemas.py                  # Core data models
├── templates/                  # Reusable templates
│   └── feedback_json.py        # Feedback formatting
└── sub_agents/                 # Agent implementations
    ├── research_pipeline_gpt.py          # Templated research pipeline
    ├── research_pipeline_schemas.py      # Pipeline schemas
    ├── company_profile_pipeline.py       # Profile extraction pipeline
    ├── company_profile_*.py              # Profile sub-agents
    └── orchestrator_*.py                 # Agent stubs
```

## Key Concepts Demonstrated

1. **Separation of Concerns**
   - Reusable pipelines vs domain-specific agents
   - Clear interfaces through schemas

2. **Template Method Pattern**
   - Base research pipeline with customizable steps
   - Builder functions for instruction composition

3. **Composition over Inheritance**
   - Agents composed of sub-agents
   - Pipelines built from smaller units

4. **ADK Best Practices**
   - Structured outputs with Pydantic
   - Session state management
   - Proper agent descriptions