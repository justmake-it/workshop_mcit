# Market Research Assistant - Test Conversations

This document contains test conversation flows to validate the market research assistant is working correctly. Use these to manually test after running `adk web`.

## What to Look For

### ✅ Good Behaviors
- Natural conversation flow without formal greetings
- Builds on previous context in the conversation
- Research happens when user shows interest
- Findings presented conversationally, not as reports
- No announcements like "Let me search for that"
- Suggests follow-up areas without being pushy

### ❌ Bad Behaviors to Watch For
- "Hello, I'm your assistant" type introductions
- Forgetting previous context between messages
- "I'll search for that for you" announcements
- Formal report-style responses
- Pushing AgentFlow as a solution
- Restarting conversation between responses

---

## Test Conversation 1: Open Exploration

### Turn 1
**You**: "I'm interested in exploring DevOps opportunities"

**Expected Response Characteristics**:
- Shows curiosity about your interests
- Mentions different industry possibilities
- Asks what aspects interest you most
- NO formal greeting or introduction

### Turn 2
**You**: "Tell me more about e-commerce challenges"

**Expected Response Characteristics**:
- Acknowledges e-commerce interest naturally
- Performs research (but doesn't announce it)
- Shares specific challenges like scaling, inventory sync, global operations
- Mentions real examples if found
- Suggests areas to explore deeper

### Turn 3
**You**: "What about during Black Friday specifically?"

**Expected Response Characteristics**:
- Builds on e-commerce context from before
- Researches peak traffic challenges
- Shares specific Black Friday/sales event issues
- Mentions cost spikes, checkout failures, etc.
- Connects findings to previous discussion

---

## Test Conversation 2: Fintech Deep Dive

### Turn 1
**You**: "What DevOps challenges do fintech companies face?"

**Expected Response Characteristics**:
- Provides initial thoughts about fintech
- Mentions compliance, scaling, security concerns
- May or may not search immediately
- Sets up for deeper exploration

### Turn 2
**You**: "How do they handle compliance while scaling quickly?"

**Expected Response Characteristics**:
- Remembers fintech context
- Searches for compliance + scaling specific info
- Shares how companies balance speed vs. regulation
- Mentions specific approaches or tools
- Natural conversation tone maintained

### Turn 3
**You**: "Can you find specific examples?"

**Expected Response Characteristics**:
- Searches for real fintech examples
- Names actual companies and their approaches
- Maintains fintech + compliance context
- Presents findings conversationally
- Might identify patterns or gaps

---

## Test Conversation 3: Gaming Industry Exploration

### Turn 1
**You**: "I've heard game developers have unique DevOps problems"

**Expected Response Characteristics**:
- Acknowledges the gaming industry interest
- Shares initial thoughts on gaming DevOps
- Mentions things like live services, updates, multiplayer
- Invites further exploration

### Turn 2
**You**: "What about mobile game testing?"

**Expected Response Characteristics**:
- Focuses on mobile gaming specifically
- Researches device fragmentation, testing challenges
- Shares findings about costs, complexity
- Mentions specific pain points

### Turn 3
**You**: "How are teams currently handling this?"

**Expected Response Characteristics**:
- Builds on mobile testing context
- Searches for current solutions/approaches
- Identifies what works and what doesn't
- Spots market gaps or opportunities
- Maintains conversational flow

---

## Test Conversation 4: Hypothesis Validation

### Turn 1
**You**: "I think e-commerce companies struggle with checkout systems during sales. Is this true?"

**Expected Response Characteristics**:
- Doesn't immediately confirm or deny
- Shows interest in exploring the hypothesis
- May share initial thoughts
- Prepares to research the specific claim

### Turn 2
**You**: "What makes checkout particularly vulnerable?"

**Expected Response Characteristics**:
- Researches checkout-specific challenges
- Explains technical bottlenecks
- Shares real examples of failures
- Maintains investigative tone
- Builds comprehensive picture

---

## Quick Validation Checklist

After each conversation, verify:

- [ ] No conversation restarts between messages
- [ ] Agent remembers what was discussed before
- [ ] Research happens naturally without announcements
- [ ] Responses feel like talking to a colleague
- [ ] User controls the direction of exploration
- [ ] Insights emerge from research, not predetermined
- [ ] No pushing of specific solutions
- [ ] Natural suggestions for follow-up topics

---

## Edge Cases to Test

1. **Vague Input**: "Tell me about stuff"
   - Should ask for clarification naturally
   - Maintain helpful tone

2. **Topic Switch**: Start with gaming, then suddenly ask about healthcare
   - Should handle transition smoothly
   - May reference previous topic if relevant

3. **Direct Question**: "What's the biggest DevOps pain point?"
   - Should explore rather than prescribe
   - Might suggest it depends on context

4. **Multiple Questions**: "What about fintech, gaming, and healthcare?"
   - Should handle systematically
   - Maintain ability to dive deeper on any