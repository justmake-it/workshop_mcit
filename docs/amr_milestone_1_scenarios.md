# Market Researcher Agent - Testing Scenarios

## Overview

These scenarios demonstrate the progressive complexity of human-AI collaboration across two milestones. Each scenario includes realistic dialogue, decision points, and expected outcomes to help workshop participants understand the collaborative nature of the system.

### Testing Philosophy
- **Milestone 1**: Focus on establishing trust through simple, transparent interactions
- **Milestone 2**: Demonstrate the power of coordinated specialist teams
- Each scenario shows specific decision points where human input shapes the outcome
- Error handling scenarios teach resilience and graceful degradation

---

## Milestone 1 Scenarios (Simple & Scoped)

### Scenario 1.1: First Conversation with Assistant

**Objective**: Establish rapport and understand the assistant's collaborative nature

**Starting Prompt**:
```
User: Hi, I need help researching gaming companies
```

**Expected Interaction Flow**:
```
Assistant: Hello! I'm your collaborative research assistant, here to help you understand gaming 
companies with DevOps challenges. I'll work with you step-by-step, asking for your guidance 
at each major decision point.

What aspect of gaming companies' DevOps challenges should I research first? For example:
- Infrastructure scaling for multiplayer games
- Deployment challenges and downtime
- Team structure and tooling
- Cost optimization
- Something else you have in mind?

User: Let's start with deployment challenges