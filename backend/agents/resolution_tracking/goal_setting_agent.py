"""
Goal Setting Agent
Takes vague user resolutions and converts them into structured, achievable plans.
"""
from typing import Dict, Any
from agents.base_agent import BaseAgent
from workflows.state import OnboardingState
from agents.constraint_framework import INDIVIDUAL_AGENT_PROMPT


class GoalSettingAgent(BaseAgent):
    """
    Agent that interprets user resolutions and creates structured plans.
    
    Responsibilities:
    - Parse vague goals ("get fit") into specific actions
    - Set realistic timelines
    - Define measurable milestones
    - Adapt to user constraints
    """
    
    def __init__(self):
        super().__init__(
            name="Goal Setting Agent",
            description="Converts vague resolutions into structured, actionable plans",
            model="llama-3.3-70b-versatile"
        )
    
    async def analyze(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze user's resolution and create structured plan.
        
        Args:
            input_data: Dict containing resolution_text and life_constraints
            
        Returns:
            Dict with goal_analysis, structured_plan, confidence_score
        """
        # Extract inputs
        resolution = input_data.get("resolution_text", "")
        constraints = input_data.get("life_constraints", [])
        occupation = input_data.get("occupation", "Not specified")
        occupation_details = input_data.get("occupation_details", {})
        user_profile = input_data.get("_user_profile", {})
        
        # Build prompts
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(resolution, constraints, occupation, occupation_details)
        
        # Add user context if available
        if self.requires_user_context and user_profile:
            context = self._build_user_context_prompt(user_profile)
            user_prompt = f"{user_prompt}\n\nUser Context: \n {context}"
        
        # Call LLM (using BaseAgent's method)
        response = await self._call_llm(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.3,
            max_tokens=1000
        )
        
        # Parse response (using BaseAgent's method)
        analysis = self._parse_json_response(response)
        
        return {
            "goal_analysis": analysis,
            "agent_name": self.name,
            "confidence_score": analysis.get("confidence", 0.0)
        }
    
    def _build_system_prompt(self) -> str:
        """Build system prompt for goal setting."""
        constraint_prompt = INDIVIDUAL_AGENT_PROMPT.format(
            agent_name="Goal Setting Agent",
            specialty="converting vague health resolutions into measurable, achievable goals"
        )
        return constraint_prompt + "\n" + """You are an expert goal-setting coach specializing in New Year's resolutions.

        Your role:
        - Convert vague resolutions into specific, measurable goals
        - Set realistic timelines based on user constraints
        - Create achievable milestones
        - Adapt plans to real-life limitations

        Key principles:
        - Start small and build up (better to succeed at small goal than fail at big one)
        - Make it specific (not "get fit", but "exercise 3x/week for 20 minutes")
        - Account for life constraints (busy schedule = shorter workouts)
        - Focus on sustainability over perfection

        You MUST respond with valid JSON in this exact format:
        {
            "original_resolution": "user's exact words",
            "interpreted_goal": "specific, measurable goal",
            "weekly_target": "concrete weekly action",
            "first_milestone": "achievable goal for first 4 weeks",
            "reasoning": "why this plan fits the user",
            "adaptations": ["how plan accounts for constraints"],
            "confidence": 0.85
        }"""
    
    def _build_user_prompt(self, resolution: str, constraints: list, occupation: str, details: dict) -> str:
        """Build user prompt with context."""
        constraints_text = ", ".join(constraints) if constraints else "None specified"
        details_text = ", ".join([f"{k}: {v}" for k, v in details.items()]) if details else "None"
        
        return f"""Analyze this resolution and create a structured plan:

        Resolution: "{resolution}"
        Occupation: {occupation}
        Job Details: {details_text}
        Life Constraints: {constraints_text}

        Create a plan that:
        1. Makes the goal specific and measurable
        2. Accounts for their constraints
        3. Starts achievable (they can always increase later)
        4. Sets a clear first milestone (4 weeks)

        Respond ONLY with valid JSON matching the required format."""


    async def process_node(self, state: OnboardingState) -> OnboardingState:
        """
        LangGraph node function.
        This is what the workflow will call.
        """
        try:
            input_data = {
                "resolution_text": state.get("resolution_text", ""),
                "life_constraints": state.get("life_constraints", []),
                "occupation": state.get("occupation"),
                "occupation_details": state.get("occupation_details")
            }

            result = await self.analyze(input_data)

            state["goal_analysis"] = result["goal_analysis"]
            state["confidence_score"] = result["confidence_score"]

            return state

        except Exception as e:
            if "errors" not in state:
                state["errors"] = []
            state["errors"].append(f"{self.name} error: {str(e)}")
            return state
