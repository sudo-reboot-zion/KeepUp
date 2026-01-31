from typing import Dict, Any
from agents.base_agent import BaseAgent
from workflows.state import OnboardingState
from memory.agent_memory import AgentMemory
import json
from agents.constraint_framework import INDIVIDUAL_AGENT_PROMPT

# agents/resolution_tracking/failure_pattern_agent.py

class FailurePatternAgent(BaseAgent):
    """
    Agent that identifies why past resolutions failed and challenges overly optimistic plans.
    
    This agent is the SKEPTIC - it looks for red flags.
    """
    
    def __init__(self):
        super().__init__(
            name="Failure Pattern Agent",
            description="Identifies failure patterns and challenges unrealistic plans",
            model="llama-3.3-70b-versatile"
        )
    
    async def analyze(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze past failures and identify risk patterns"""
        
        past_attempts = input_data.get("past_attempts", "")
        goal_analysis = input_data.get("goal_analysis", {})
        user_profile = input_data.get("_user_profile", {})
        user_memory = input_data.get("user_memory", {})
        
        # Format memory for prompt
        memory_context = ""
        if user_memory:
            failures = user_memory.get("by_type", {}).get("failure_pattern", [])
            if failures:
                memory_context = "\nKNOWN FAILURE PATTERNS (from memory):\n" + "\n".join(
                    [f"- {f['content'].get('pattern', '')}" for f in failures[:5]]
                )
        
        constraint_prompt = INDIVIDUAL_AGENT_PROMPT.format(
            agent_name="Failure Pattern Agent",
            specialty="identifying risk factors and failure patterns in health goal attempts"
        )
        system_prompt = constraint_prompt + "\n" + """You are a failure pattern expert who has studied thousands of abandoned resolutions.

        Your role:
        - Identify why past attempts failed
        - Spot red flags in new plans
        - Predict quit probability
        - Suggest protective guardrails

        Common failure patterns:
        - Week 3 cliff (most people quit week 3-4)
        - Overcommitment (starting too ambitious)
        - Life event collision (didn't plan for disruptions)
        - Motivation depletion (relied on willpower alone)
        - All-or-nothing thinking (missed one day → quit entirely)

        Respond with JSON:
        {
            "identified_patterns": ["pattern 1", "pattern 2"],
            "quit_probability": 0.65,
            "highest_risk_period": "Week 3-4",
            "protective_strategies": ["strategy 1", "strategy 2"],
            "plan_concerns": ["concern about proposed plan"],
            "recommended_adjustments": ["make it easier", "add buffer"],
            "confidence": 0.80
        }"""
        
        user_prompt = f"""Past Attempts: {past_attempts}

        Proposed Plan: {json.dumps(goal_analysis, indent=2)}
        {memory_context}

        Analyze failure risk and suggest protective adjustments."""
        
        # Add user context if available
        if self.requires_user_context and user_profile:
            context = self._build_user_context_prompt(user_profile)
            user_prompt = f"{user_prompt}\n\nUser Context: \n {context}"
        
        response = await self._call_llm(system_prompt, user_prompt)
        analysis = self._parse_json_response(response)
        
        # Check if we should add this as a learning to state
        # If this is being called from a workflow with state, add learnings
        if "state" in input_data and analysis.get("identified_patterns"):
            state = input_data["state"]
            AgentMemory.add_learning_to_state(
                state,
                agent_name=self.name,
                learning_type="failure_pattern",
                content={
                    "patterns": analysis.get("identified_patterns", []),
                    "quit_probability": analysis.get("quit_probability", 0.0),
                    "highest_risk_period": analysis.get("highest_risk_period", ""),
                    "protective_strategies": analysis.get("protective_strategies", [])
                },
                confidence=analysis.get("confidence", 0.8),
                expires_after_days=90  # Keep for 90 days
            )
        
        return {
            "failure_risk": analysis,
            "agent_name": self.name,
            "confidence_score": analysis.get("confidence", 0.0)
        }
    
    async def process_node(self, state: OnboardingState) -> OnboardingState:
        """Process node for LangGraph"""
        try:
            # Read past learnings from state memory
            past_patterns = AgentMemory.get_memory_from_state(
                state,
                learning_type="failure_pattern"
            )
            
            input_data = {
                "past_attempts": state.get("past_attempts", ""),
                "goal_analysis": state.get("goal_analysis", {}),
                "state": state  # Pass state so analyze() can add learnings
            }
            
            # Include past learnings in the prompt if available
            if past_patterns:
                input_data["past_learnings"] = past_patterns
            
            result = await self.analyze(input_data)
            state["failure_risk"] = result["failure_risk"]
            
            # Now CHALLENGE the goal setting agent's plan
            if state.get("goal_analysis"):
                challenge_result = await self.challenge(
                    proposed_plan=state["goal_analysis"],
                    challenger_context={"past_attempts": state.get("past_attempts")}
                )
                state["failure_agent_challenge"] = challenge_result
            
            return state
            
        except Exception as e:
            if "errors" not in state:
                state["errors"] = []
            state["errors"].append(f"{self.name} error: {str(e)}")
            return state
