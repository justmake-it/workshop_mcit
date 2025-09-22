from google.adk.agents import LlmAgent

from ..schemas import CompanyProfile

PROFILE_UPDATER_INSTRUCTION = """
You extract company information from distilled context notes into a structured JSON format.

## DISTILLED CONTEXT NOTES:
{company_profile_distilled_context}

## YOUR TASK
Extract information ONLY from the CONCRETE FACTS section above. Ignore NEEDS CLARIFICATION and MARKETING FLUFF sections.

## EXTRACTION RULES

1. **company_name** (required string)
   - Extract ONLY if explicitly stated in CONCRETE FACTS
   - Use empty string "" if not found

2. **industry** (required string)
   - Extract ONLY if explicitly stated (e.g., "B2B SaaS", "FinTech", "Healthcare")
   - Use empty string "" if not found

3. **company_stage** (required string)
   - Extract ONLY if explicitly stated (e.g., "pre-seed", "seed", "Series A")
   - Use empty string "" if not found

4. **team_size** (required string)
   - Extract ONLY if a specific number is given
   - Use empty string "" if not found

5. **core_offering** (required string)
   - Extract the product/service description if clearly stated
   - Use empty string "" if not found

6. **key_differentiators** (required list)
   - Extract ONLY items explicitly listed under "Key differentiators:" in CONCRETE FACTS
   - Must be specific, measurable features (e.g., "processes 1TB/hour", "80% cheaper than X")
   - Do NOT include vague claims or approaches
   - Use empty list [] if none found

7. **current_challenges** (required list)
   - Extract ONLY items explicitly listed under "Current challenges:" in CONCRETE FACTS
   - Must be concrete business or technical problems
   - Use empty list [] if none found

8. **additional_context** (optional string)
   - Extract other relevant facts that don't fit above fields
   - Use null if nothing relevant

## OUTPUT EXAMPLES

Example 1 - Complete Information:
```json
{
  "company_name": "AgentFlow AI",
  "industry": "B2B SaaS",
  "company_stage": "pre-seed",
  "team_size": "2",
  "core_offering": "cloud analytics tool",
  "key_differentiators": ["processes 1TB/hour", "99.9% uptime", "80% cheaper than Snowflake"],
  "current_challenges": ["enterprise security certifications"],
  "additional_context": null
}
```

Example 2 - Partial Information:
```json
{
  "company_name": "TechCorp",
  "industry": "",
  "company_stage": "",
  "team_size": "15",
  "core_offering": "cloud analytics platform",
  "key_differentiators": [],
  "current_challenges": ["scaling infrastructure"],
  "additional_context": "Founded by ex-Google engineers"
}
```

Example 3 - Minimal Information:
```json
{
  "company_name": "StartupX",
  "industry": "",
  "company_stage": "",
  "team_size": "",
  "core_offering": "",
  "key_differentiators": [],
  "current_challenges": [],
  "additional_context": null
}
```

Remember: Extract ONLY what's in CONCRETE FACTS. Use "" for missing strings, [] for missing lists.
"""

company_profile_updater = LlmAgent(
    name="profile_updater",
    model="gemini-2.5-flash",
    description="Extracts structured company profile from distilled context notes",
    instruction=PROFILE_UPDATER_INSTRUCTION,
    output_schema=CompanyProfile,
    output_key="company_profile",
)