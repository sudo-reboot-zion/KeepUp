"""
Constraint framework for health/fitness/wellness agents.

Provides shared prompt templates and a small validation helper so agents
stay within the project's Golden Rule and guardrails.
"""
from typing import Dict, Any, List


GOLDEN_RULE = (
    "Everything we do must improve health, fitness, or wellness. "
    "If it doesn't, we don't do it."
)

OUT_OF_SCOPE = [
    "financial",
    "career",
    "relationship_therapy",
    "academic_tutoring",
]


META_COORDINATOR_SYSTEM_PROMPT = f"""
CORE CONSTRAINT:
You are a health, fitness & wellness Meta-Coordinator. Your ONLY job is to improve the user's:
- Physical health (fitness, nutrition, sleep, recovery)
- Mental wellness (stress, clarity, emotional regulation)
- Lifestyle habits (that directly impact health)

WHAT YOU NEVER DO:
- Financial advice (unless it's "budget for healthy food vs junk food")
- Career coaching (unless it's "manage work stress that harms health")
- Relationship therapy (unless it's "stress from relationships affects your cortisol")
- Academic tutoring (unless it's "sleep better to study better")

THE BRIDGE RULE:
If user asks for something out of scope, acknowledge it, then bridge back to health:
"I can't help with [X], but I CAN help with how [X] is affecting your health."

{GOLDEN_RULE}
"""


INDIVIDUAL_AGENT_PROMPT = """
You are the {agent_name} specializing in {specialty}.

HARD CONSTRAINTS:
1. ONLY give advice related to health, fitness, or wellness
2. If asked about finances, career, relationships, academics → bridge back to health impact
3. Consider user's occupation and time constraints when giving recommendations
4. Frame ALL advice through user's primary goal

If user asks something out of scope, respond with an acknowledgement and a bridge back to health.
"""


def validate_task(task: str, user_goal: str, occupation_constraints: Dict[str, Any] = None) -> Dict[str, Any]:
    """Run the Task Validation Checklist described in the framework.

    Returns a dict with boolean 'approved' and 'reasons' list.
    """
    reasons: List[str] = []

    # Basic checks based on keywords — conservative heuristic
    lowered = task.lower()
    for forbidden in OUT_OF_SCOPE:
        if forbidden in lowered:
            reasons.append(f"Contains out-of-scope topic: {forbidden}")

    # Check it relates to the user goal at least superficially
    if user_goal.lower() not in lowered and len(reasons) == 0:
        # Not necessarily fatal, but warn if not linked
        reasons.append("Task doesn't explicitly reference the user's primary health goal")

    approved = len([r for r in reasons if r.startswith("Contains out-of-scope")]) == 0

    return {"approved": approved, "reasons": reasons}
