"""
Test Scenarios for Workshop 2: GTM Intelligence System

These scenarios demonstrate different ways the system handles various inputs,
from minimal context to rich company profiles.
"""

# SCENARIO 1: Minimal Input
# -------------------------
# User provides almost no context, system guides discovery
MINIMAL_INPUT = {
    "user_message": "I'm building a DevOps platform",
    "expected_behavior": """
    1. Research Collector starts with broad discovery questions
    2. Multiple iterations (3-5) to gather enough information
    3. Validator identifies many missing fields initially
    4. System gradually builds complete ICP through conversation
    """,
    "teaching_points": [
        "LoopAgent handles vague inputs gracefully",
        "State accumulates across iterations",
        "Validator guides the research process"
    ]
}

# SCENARIO 2: Rich Context (AgentFlow Profile)
# -------------------------------------------
# User provides comprehensive company profile
RICH_CONTEXT = {
    "user_message": """
    We're AgentFlow AI, a pre-seed DevOps startup. We predict CI/CD pipeline 
    failures with 73% accuracy using AI. Founded by ex-Paddle and ex-Google 
    engineers. Targeting gaming studios (100-500 employees) who lose $100K+ 
    per hour during launch failures. Our solution costs 80% less than Datadog 
    at $500-2000/month. Main competitors: Datadog (reactive, expensive), 
    PagerDuty (incident response only).
    """,
    "expected_behavior": """
    1. Research Collector recognizes rich context
    2. Only 1-2 iterations needed
    3. ICP Writer extracts comprehensive structure immediately
    4. Validator finds few gaps, mainly asks for clarification
    """,
    "teaching_points": [
        "System adapts to context depth",
        "Fewer iterations when more data provided",
        "include_contents='none' speeds up processing"
    ]
}

# SCENARIO 3: Pivot Mid-Research
# ------------------------------
# Company changes direction during ICP development
PIVOT_SCENARIO = {
    "initial_message": "We're building a DevOps tool for gaming companies",
    "pivot_message": "Actually, we've decided to focus on e-commerce instead of gaming",
    "expected_behavior": """
    1. Initial iterations build gaming-focused ICP
    2. Pivot triggers new research direction
    3. Validator identifies need to update all segments
    4. System adapts without starting over
    """,
    "teaching_points": [
        "State management handles changes gracefully",
        "LoopAgent can adapt mid-process",
        "Memory of previous work isn't lost"
    ]
}

# SCENARIO 4: Testing Loop Termination
# -----------------------------------
# Demonstrate what happens without proper escalate=True
LOOP_TERMINATION_TEST = {
    "setup": "Temporarily comment out EventActions(escalate=True) in validator",
    "expected_behavior": """
    1. Loop continues even when ICP is complete
    2. Runs until max_iterations (5) is reached
    3. System still works but wastes iterations
    """,
    "teaching_points": [
        "escalate=True is critical for efficiency",
        "max_iterations prevents infinite loops",
        "Proper termination saves time and tokens"
    ]
}

# SCENARIO 5: Session State Persistence
# -------------------------------------
# Show how state persists within a session
SESSION_STATE_SCENARIO = {
    "first_request": "I'm building a DevOps platform for gaming studios",
    "second_request": "Can you remind me what we discussed about my target market?",
    "expected_behavior": """
    1. First request: Full research process (3-5 iterations)
    2. ICP stored in session state
    3. Second request: Orchestrator can access previous ICP from state
    4. No need to rebuild ICP from scratch within same session
    """,
    "teaching_points": [
        "State persists within a session",
        "Agents can access previous work via state",
        "Session state acts as short-term memory"
    ]
}

# COMMON ISSUES AND FIXES
# ----------------------
COMMON_ISSUES = {
    "state_not_updating": {
        "symptom": "Agent outputs don't appear in state",
        "cause": "Typo in output_key name",
        "fix": "Check exact output_key spelling matches state access"
    },
    "loop_wont_end": {
        "symptom": "Loop runs all 5 iterations even when complete",
        "cause": "Missing EventActions(escalate=True)",
        "fix": "Ensure validator returns Event with escalate=True"
    },
    "slow_processing": {
        "symptom": "Each iteration takes 30+ seconds",
        "cause": "Using include_contents='default' for all agents",
        "fix": "Set include_contents='none' for ICP Writer and Validator"
    },
    "empty_icp": {
        "symptom": "ICP has many None/empty fields",
        "cause": "Research findings not comprehensive enough",
        "fix": "Improve Research Collector prompts to gather more data"
    }
}

# WORKSHOP DEMO FLOW
# -----------------
def print_demo_flow():
    """Print the recommended demo flow for the workshop."""
    print("""
    🎯 WORKSHOP DEMO FLOW (120 minutes)
    ===================================
    
    1. OPENING DEMO (5 min)
       - Show final system with minimal input → complete ICP
       - "Look what we'll build in the next 2 hours!"
    
    2. BUILD RESEARCH COLLECTOR (25 min)
       - Start with manual state management (show pain)
       - Add output_key (show magic!)
       - Test with simple input
    
    3. BUILD ICP WRITER (20 min)  
       - Define schema (explain structure)
       - Show tools OR schemas constraint
       - Add include_contents='none' (time the difference!)
    
    4. BUILD QUALITY VALIDATOR (15 min)
       - Implement validation logic
       - CRITICAL: Add EventActions(escalate=True)
       - Test without it first (show infinite loop risk)
    
    5. ASSEMBLE LOOPAGENT (20 min)
       - Connect all three agents
       - Explain iteration flow
       - Run first complete test
    
    6. ADD ORCHESTRATOR (15 min)
       - Quick routing implementation  
       - Show memory integration
       - Discuss future extensions
    
    7. TEST SCENARIOS (20 min)
       - Minimal input test
       - Rich context test  
       - Let participants try their companies
    
    8. WRAP-UP (5 min)
       - Recap key concepts
       - Share resources
       - Preview next workshop
    
    💡 Keep energy high! Celebrate each working component!
    """)

# PARTICIPANT EXERCISES
# --------------------
EXERCISES = [
    {
        "title": "Exercise 1: Add a New Validation Rule",
        "task": "Add a check for minimum 2 competitors in the validator",
        "hint": "Update quality_validator instruction and validation logic",
        "learning": "Understanding how to extend validation criteria"
    },
    {
        "title": "Exercise 2: Create Industry-Specific Researcher", 
        "task": "Create a gaming_researcher variant with gaming-specific questions",
        "hint": "Copy research_collector and customize instruction",
        "learning": "How to specialize agents for verticals"
    },
    {
        "title": "Exercise 3: Add Completeness Visualization",
        "task": "Create a progress bar showing ICP completeness",
        "hint": "Use state_helpers.py and validation_result data",
        "learning": "Working with state data for UI/monitoring"
    }
]

if __name__ == "__main__":
    print_demo_flow()