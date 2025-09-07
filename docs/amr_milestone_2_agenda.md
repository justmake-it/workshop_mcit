# Workshop 2: GTM Intelligence System - Speaker Notes

**Duration**: 2 hours | **Format**: Live coding workshop

---

## OPENING (5 min)

### What We're Building

• **Market Research Agent** that works for ANY company

- Current: Hardcoded for AgentFlow
- New: Accepts any company description
- Uses LoopAgent for iterative ICP development

### Based on Real ADK Patterns

• **LoopAgent**: Like ADK's Gemini Fullstack research & critique loop
• **Context Building**: Like ADK's Financial Advisor (ticker → risk → strategy)
• **Validation Loop**: Quality validator guides next iteration

**[QUICK DEMO: Show end result]**

---

## ROADMAP (2 min)

### What We'll Build (120 min total)

1. **GTM Orchestrator** (15 min) → Routing
2. **Research Collector** (25 min) → Learn output_key
3. **ICP Writer** (20 min) → Learn include_contents
4. **Quality Validator** (15 min) → Learn loop control
5. **LoopAgent** (20 min) → Orchestration
6. **Testing** (20 min) → See it work
7. **Wrap-up** (5 min)

**[START CODING IMMEDIATELY]**

## BUILD: GTM ORCHESTRATOR (15 min)

### The Router

• User input → Right specialist
• Context awareness
• Memory integration

### Quick Implementation

```
gtm_orchestrator = LlmAgent(
    name="gtm_orchestrator",
    model="gemini-2.5-pro",
    sub_agents=[market_researcher],
    instruction="Route to market researcher"
)
```

### Key Features

**[ADD AS WE CODE]**

• Pro model for routing
• Memory search tool
• Transfer capabilities
• Context checking

### State Management

• Read validation feedback
• Check existing context
• Route to appropriate agent

### Future Extensions

**[QUICK PREVIEW]**

• Add content_creator
• Add outreach_specialist  
• Full GTM pipeline

**[TRANSITION: "Let's build the components..."]**

## BUILD: RESEARCH COLLECTOR (25 min)

### Setup

**[LIVE CODING STARTS]**

• Create folder structure
• Start with basic LlmAgent

### First Implementation

```
research_collector = LlmAgent(
    name="research_collector",
    model="gemini-2.5-flash",
    tools=[google_search]
)
```

### The Problem

• How to save research findings?
• Manual state management is painful

### Introduce: output_key

**[CONCEPT AS WE CODE]**

• Add `output_key="research_findings"`
• ADK automatically saves to state
• No manual ctx.state["key"] = value

### Enhanced Implementation

• Add description
• Add instruction  
• Test basic conversation

**[CHECKPOINT: Collector working]**

### Key Learning

• output_key = automatic state management
• State persists between iterations
• Clean, functional design

**[TRANSITION: "Now transform research to ICP..."]**

## BUILD: ICP WRITER (20 min)

### The Need

• Research findings = unstructured text
• Need structured ICP output
• ADK constraint: Tools OR schemas

### Basic Implementation

```
icp_writer = LlmAgent(
    name="icp_writer",
    model="gemini-2.5-flash",
    output_schema=ICPSchema
)
```

### The Performance Question

• Does it need conversation history?
• Just needs research findings from state

### Introduce: include_contents

**[CONCEPT AS WE CODE]**

• `include_contents='none'`
• Only reads from state
• 2-3x faster processing
• Add output_key="icp_draft"

### Complete Implementation

• Define ICPSchema
• Add transformation instruction
• Test with mock research data

**[DEMO: State flow visualization]**

### Key Learning

• Separation: tools vs schemas
• include_contents optimization
• Functional pipeline pattern

**[TRANSITION: "But how do we know ICP is complete?"]**

## BUILD: QUALITY VALIDATOR (15 min)

### The Loop Problem

• When to stop iterating?
• How to guide next iteration?

### Basic Implementation

```
quality_validator = LlmAgent(
    name="quality_validator",
    model="gemini-2.5-flash",
    include_contents='none',
    output_key="validation_result"
)
```

### Validation Logic

• Check ICP completeness
• Identify missing fields
• Generate next questions

### Introduce: Loop Termination

**[CRITICAL CONCEPT]**

• EventActions(escalate=True)
• Properly exits LoopAgent
• Prevents infinite loops

### Complete Implementation

• Add validation instruction
• Set is_complete flag
• Generate specific gaps

**[TEST: Run validation on partial ICP]**

### Key Learning

• Validators guide iteration
• Proper loop termination
• State-driven decisions

**[TRANSITION: "Time to orchestrate these agents..."]**

## BUILD: LOOPAGENT ORCHESTRATION (20 min)

### The Pattern

• Three agents work together
• Each iteration improves ICP
• Automatic state flow

### Implementation

```
market_researcher = LoopAgent(
    name="market_researcher_loop",
    sub_agents=[
        research_collector,
        icp_writer,
        quality_validator
    ],
    max_iterations=5
)
```

### How It Works

**[VISUALIZE ON BOARD]**

Iteration 1:
• Collector → research_findings
• Writer → icp_draft
• Validator → "missing: [pricing, competitors]"

Iteration 2:
• Collector reads missing fields
• Asks targeted questions
• Improved ICP

### Iterative Refinement Demo

**[LIVE TEST]**

• Start: "I build DevOps tools"
• Watch state evolution
• Validator identifies gaps
• Research collector fills them
• Complete ICP in 3-5 iterations

**[CELEBRATE: Working market researcher!]**

## TESTING THE SYSTEM (20 min)

### Test Scenarios

**Scenario 1: Minimal Input**
• "I'm building a DevOps platform"
• Watch iterative refinement
• Validator guides questions
• 3-5 iterations to complete ICP

**Scenario 2: Rich Context**
• Paste company profile
• Fast validation
• 1-2 iterations only

### Live Debugging

**[COMMON ISSUES]**

• State not updating → Check output_key
• Loop won't end → Add escalate=True
• Slow processing → Use include_contents='none'

### Memory Preview

**[IF TIME ALLOWS]**

• Show memory search
• Demonstrate acceleration
• Future possibilities

**[PARTICIPANT TESTS]**

## WRAP-UP (5 min)

### What We Built

• Market researcher that handles ANY company
• LoopAgent iterative refinement
• State-driven validation

### Key Takeaways

• **output_key** → Automatic state management
• **include_contents** → Performance optimization
• **LoopAgent** → Iterative refinement
• **EventActions** → Proper termination

### Next Steps

• Add memory integration
• Build content creator
• Deploy to production

**[SHARE: Code repository link]**

---

## FACILITATOR NOTES

**Time Management**
• Stay in code editor
• Introduce concepts while typing
• Keep momentum high

**If Running Behind**
• Skip GTM orchestrator
• Focus on core loop
• Test with simple inputs

**Key Success Factors**
• Working code > perfect code
• Concepts through practice
• Celebrate small wins
