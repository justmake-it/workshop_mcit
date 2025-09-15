# Workshop 2: GTM Intelligence System

A company-agnostic market research system built with Google's Agent Development Kit (ADK).

## 🎯 Learning Objectives

By the end of this workshop, you'll understand:

1. **LoopAgent**: How to build iterative refinement systems
2. **output_key**: Automatic state management without manual updates  
3. **include_contents**: Performance optimization for stateless agents
4. **EventActions(escalate=True)**: Proper loop termination
5. **Multi-agent orchestration**: Building complex systems from simple agents

## 🏗️ What We're Building

Transform the hardcoded AgentFlow market researcher into a flexible system that:
- Works for ANY company (not just AgentFlow)
- Iteratively refines ICPs through validation loops
- Maintains context within the session via state
- Scales to support content creation and outreach (future workshops)

## 📁 Project Structure

```
02_gtm_intelligence/
├── agent.py              # Main orchestrator with LoopAgent
├── schemas.py            # ICPSchema definition
├── prompts.py            # Agent instructions
├── sub_agents/
│   ├── research_collector.py  # Gathers market data (has tools)
│   ├── icp_writer.py         # Structures data (has schema)
│   └── quality_validator.py  # Validates & controls loop
└── test_scenarios.py         # Workshop test cases
```

## 🚀 Quick Start

```python
# Test the system
from agents.workshops.02_gtm_intelligence import root_agent

# Minimal input
response = await root_agent.run("I'm building a DevOps platform")

# Rich context  
response = await root_agent.run("""
We're AgentFlow AI, targeting gaming studios with 
AI-powered pipeline failure prediction...
""")
```

## 🔑 Key Concepts Demonstrated

### 1. Automatic State Management (output_key)

```python
research_collector = LlmAgent(
    name="research_collector",
    output_key="research_findings",  # Auto-saves to state!
    # No more: ctx.state["research_findings"] = result
)
```

### 2. Performance Optimization (include_contents)

```python
icp_writer = LlmAgent(
    name="icp_writer",
    include_contents='none',  # 2-3x faster!
    # Only reads from state, skips conversation history
)
```

### 3. Loop Control (EventActions)

```python
# In validator instruction:
"When complete, return: Event(
    content='ICP complete', 
    actions=EventActions(escalate=True)
)"
```

### 4. Iterative Refinement (LoopAgent)

```python
market_researcher = LoopAgent(
    sub_agents=[collector, writer, validator],
    max_iterations=5  # Safety limit
)
```

## 📊 Data Flow

```
Iteration 1:
Research Collector → state["research_findings"]
    ↓
ICP Writer → state["icp_draft"] 
    ↓
Quality Validator → state["validation_result"] = {missing: [...]}

Iteration 2:
Research Collector (reads missing fields) → enhanced findings
    ↓
ICP Writer → improved ICP
    ↓  
Quality Validator → complete + escalate=True

LOOP TERMINATES ✅
```

## 🧪 Test Scenarios

1. **Minimal Input**: "I build DevOps tools" → Full ICP in 3-5 iterations
2. **Rich Context**: Complete company profile → ICP in 1-2 iterations
3. **Session State**: Context persists within the same session
4. **Loop Termination**: Remove escalate=True → See infinite loop risk

## 🐛 Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| State not updating | Typo in output_key | Check exact spelling |
| Loop won't end | Missing escalate=True | Add to validator |
| Slow processing | include_contents='default' | Use 'none' where possible |
| Empty ICP fields | Weak research prompts | Enhance collector instruction |

## 🔧 Workshop Extensions

### Add Industry Specialists
```python
gaming_researcher = LoopAgent(
    sub_agents=[gaming_collector, icp_writer, validator]
)
```

### Add Downstream Pipelines
```python
content_pipeline = SequentialAgent(
    sub_agents=[content_analyzer, strategist, validator]
)
```

### Add State Management
```python
# Access state within agents
current_icp = tool_context.state.get("icp_draft")

# Store data in state
tool_context.state["company_profile"] = profile_data
```

## 📚 Resources

- [ADK Documentation](https://google.github.io/adk-docs/)
- [LoopAgent Guide](https://google.github.io/adk-docs/agents/workflow-agents/loop-agents/)
- [State Management](https://google.github.io/adk-docs/sessions/state/)
- [ADK Samples](https://github.com/google/adk-samples)

## 🎓 Key Takeaways

1. **output_key** eliminates manual state management
2. **include_contents='none'** boosts performance for stateless tasks
3. **EventActions(escalate=True)** properly terminates loops
4. **LoopAgent** enables sophisticated iterative workflows
5. ADK patterns scale from simple to complex systems

## 🚀 Next Steps

- Workshop 3: Content Creator Pipeline
- Workshop 4: Outreach Specialist  
- Workshop 5: Full GTM System Integration

---

Built with ❤️ using Google's Agent Development Kit