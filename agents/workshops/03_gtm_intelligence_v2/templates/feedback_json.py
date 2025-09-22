"""Template for Feedback schema JSON output."""
import json
from typing import List

# Template constants (private - not exported)
_FEEDBACK_JSON_OUTPUT_REQUIREMENTS = """
**CRITICAL: Output Requirements**
- You MUST respond with ONLY valid JSON
- Do NOT include any explanatory text before or after the JSON
- Output MUST conform to the Feedback schema exactly
- Use null for follow_up_queries when grade is "pass"
"""

_FEEDBACK_JSON_EXAMPLES = """
## JSON Output Examples:

### Example 1 - Evaluation PASSES:
```json
{{
  "grade": "pass",
  "comment": "{pass_comment}",
  "follow_up_queries": null
}}
```

### Example 2 - Evaluation FAILS:
```json
{{
  "grade": "fail",
  "comment": "{fail_comment}",
  "follow_up_queries": {follow_up_queries}
}}
```
"""

_FEEDBACK_JSON_REMINDER = """
Remember: Output ONLY the JSON object. No other text.
"""


def build_feedback_evaluator_instruction(
    role_description: str,
    evaluation_criteria: str,
    pass_example_comment: str,
    fail_example_comment: str,
    fail_example_queries: List[str]
) -> str:
    """Build a complete evaluator instruction with JSON output requirements for Feedback schema.
    
    Args:
        role_description: What the evaluator does
        evaluation_criteria: Specific criteria for evaluation
        pass_example_comment: Example comment for passing evaluation
        fail_example_comment: Example comment for failing evaluation
        fail_example_queries: Example follow-up questions for failures
    
    Returns:
        Complete instruction string with JSON formatting requirements
    """
    # Format the examples
    examples = _FEEDBACK_JSON_EXAMPLES.format(
        pass_comment=pass_example_comment,
        fail_comment=fail_example_comment,
        follow_up_queries=json.dumps(fail_example_queries, indent=4)
    )
    
    # Combine all parts
    return f"""{role_description}

{_FEEDBACK_JSON_OUTPUT_REQUIREMENTS}

{examples}

{evaluation_criteria}

{_FEEDBACK_JSON_REMINDER}"""