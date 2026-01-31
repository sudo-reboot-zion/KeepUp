"""
Meta-Coordinator Agent
Synthesizes debates between agents and makes final decisions.
"""
from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from workflows.state import OnboardingState
import json
from agents.constraint_framework import META_COORDINATOR_SYSTEM_PROMPT



class MetaCoordinator(BaseAgent):
    """
    The Judge - Synthesizes multi-agent debates into final decisions.
    
    Responsibilities:
    - Weigh competing agent recommendations
    - Balance ambition vs. safety
    - Create hybrid solutions
    - Explain reasoning transparently
    """
    
    def __init__(self):
        super().__init__(
            name="Meta-Coordinator",
            description="Synthesizes multi-agent debates and makes final coordinated decisions",
            model="llama-3.3-70b-versatile"
        )
    
    async def analyze(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Required by BaseAgent - delegates to synthesize_debate
        """
        debate_history = input_data.get("debate_history", [])
        return await self.synthesize_debate(debate_history)


    async def synthesize_debate(self, debate_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Synthesize a debate between multiple agents.
        """
        system_prompt = META_COORDINATOR_SYSTEM_PROMPT + "\n" + """You are the Meta-Coordinator - the final decision maker who synthesizes debates between specialized AI agents.

Your role:
- Weigh each agent's domain expertise
- Balance competing priorities (ambition vs. safety, short-term vs. long-term)
- Create hybrid solutions that satisfy multiple concerns
- ALWAYS explain your reasoning transparently
- Favor safety over ambition when past failures indicate risk

Key principles:
- Failure Pattern Agent challenges should be taken VERY seriously (they prevent repeating mistakes)
- Goal Setting Agent provides the aspiration (what user wants)
- Your job is to find the sweet spot that's both motivating AND sustainable
- When agents disagree, don't just pick one - create a synthesis

You MUST respond with EXACTLY this JSON format (no extra text):
{{
    "final_decision": {{
        "interpreted_goal": "specific goal statement",
        "weekly_target": "concrete weekly action",
        "first_milestone": "achievable 4-week goal",
        "reasoning": "detailed explanation of your synthesis"
    }},
    "debate_summary": {{
        "goal_agent_position": "summary of what Goal Setting Agent proposed",
        "failure_agent_position": "summary of what Failure Pattern Agent challenged",
        "synthesis_rationale": "explanation of how you balanced both positions"
    }},
    "safety_adjustments": ["list of changes made to protect user from past failures"],
    "growth_path": "how user can increase difficulty over time",
    "confidence": 0.90
}}

CRITICAL: All three keys in debate_summary MUST be present with actual content, not null!"""
        
        # Build a clearer user prompt
        user_prompt = f"""Here is the agent debate for a user with PRIMARY GOAL: {primary_goal.upper()}

GOAL SETTING AGENT PROPOSAL:
{json.dumps(debate_history[0], indent=2)}

FAILURE PATTERN AGENT CHALLENGE:
{json.dumps(debate_history[1], indent=2)}

Your task:
1. Summarize what each agent proposed
2. Identify the key conflict between their positions
3. Create a synthesis that honors both perspectives but weights them according to the {primary_goal} goal
4. Explain your reasoning clearly

Generate the JSON response now."""
        
        response = await self._call_llm(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.4,
            max_tokens=1500
        )

        # 🔍 DEBUG: Print raw response
        print("\\n" + "="*70)
        print("🔍 DEBUG - Raw LLM Response:")
        print(response)
        print("="*70 + "\\n")

        parsed = self._parse_json_response(response)
    
        # 🔍 DEBUG: Print parsed result
        print("\\n" + "="*70)
        print("🔍 DEBUG - Parsed JSON:")
        print(json.dumps(parsed, indent=2))
        print("="*70 + "\\n")
        
        
        # Safety check: ensure debate_summary exists with all keys
        if "debate_summary" not in parsed or parsed["debate_summary"] is None:
            parsed["debate_summary"] = {
                "goal_agent_position": "Summary unavailable",
                "failure_agent_position": "Summary unavailable", 
                "synthesis_rationale": "Summary unavailable"
            }
        
        return parsed
    
async def process_node(self, state: OnboardingState) -> OnboardingState:
        """
        LangGraph node - synthesizes all agent inputs into final plan.
        """
        try:
            # Gather the debate
            debate_history = [
                {
                    "agent": "Goal Setting Agent",
                    "role": "Proposes ambitious plan",
                    "output": state.get("goal_analysis", {})
                },
                {
                    "agent": "Failure Pattern Agent",
                    "role": "Challenges and identifies risks",
                    "output": state.get("failure_risk", {}),
                    "challenge": state.get("failure_agent_challenge", {})
                }
            ]
            
            # Extract primary goal
            primary_goal = state.get("primary_goal", "wellness")
            
            # Synthesize
            synthesis = await self.synthesize_debate(debate_history, primary_goal)
            
            # Store final decision
            state["final_plan"] = synthesis.get("final_decision", {})
            state["debate_summary"] = synthesis.get("debate_summary", {})
            state["safety_adjustments"] = synthesis.get("safety_adjustments", [])
            state["confidence_score"] = synthesis.get("confidence", 0.0)
            
            return state
            
        except Exception as e:
            if "errors" not in state:
                state["errors"] = []
            state["errors"].append(f"{self.name} error: {str(e)}")
            return state
