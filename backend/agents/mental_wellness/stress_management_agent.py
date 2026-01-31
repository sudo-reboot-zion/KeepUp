"""
Stress Management Agent
Recommends stress interventions and coping strategies
"""
from typing import Dict, Any
from agents.base_agent import BaseAgent
from agents.constraint_framework import INDIVIDUAL_AGENT_PROMPT


class StressManagementAgent(BaseAgent):
    """
    Recommends stress management interventions
    
    Responsibilities:
    - Detect stress levels from user input or biometrics
    - Recommend appropriate interventions
    - Provide coping strategies
    - Adjust workout intensity based on stress
    - Cortisol management techniques
    """
    
    def __init__(self):
        super().__init__(
            name="Stress Management Agent",
            description="Recommends interventions for high-stress periods",
            model="llama-3.3-70b-versatile"
        )
    
    async def analyze(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recommend stress interventions
        
        Input:
            - stress_level: str (low, moderate, high, chronic)
            - stress_source: str (work, family, health, financial, etc.)
            - current_activities: List[str] (what user is currently doing)
            - primary_goal: str (fitness, sleep, stress, wellness)
            - context: Dict (sleep, energy, etc.)
            
        Returns:
            - recommendation: str
            - rationale: str
            - avoid: List[str]
            - alternatives: List[str]
            - confidence: float
        
        Options:
        - Reduce workout intensity
        - Add meditation/breathwork
        - Focus on restorative exercises
        - Increase rest days
        """
        
        # Extract inputs
        stress_level = input_data.get("stress_level", "moderate")
        stress_source = input_data.get("stress_source", "unknown")
        current_activities = input_data.get("current_activities", [])
        primary_goal = input_data.get("primary_goal", "wellness")
        context = input_data.get("context", {})
        
        # Build prompts
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(
            stress_level, stress_source, current_activities, primary_goal, context
        )
        
        # Call LLM
        response = await self._call_llm(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.3,
            max_tokens=1000
        )
        
        result = self._parse_json_response(response)
        
        return {
            "recommendation": result.get("recommendation", ""),
            "rationale": result.get("rationale", ""),
            "avoid": result.get("avoid", []),
            "alternatives": result.get("alternatives", []),
            "breathing_exercises": result.get("breathing_exercises", []),
            "confidence": result.get("confidence", 0.0),
            "agent_name": self.name
        }
    
    def _build_system_prompt(self) -> str:
        """Build system prompt for stress management"""
        constraint_prompt = INDIVIDUAL_AGENT_PROMPT.format(
            agent_name="Stress Management Agent",
            specialty="recommending evidence-based stress interventions and cortisol management"
        )
        return constraint_prompt + """

You are a stress management expert specializing in the mind-body connection.

Your role:
- Assess stress levels and recommend appropriate interventions
- Balance exercise and stress (high stress + high intensity = cortisol overload)
- Provide evidence-based coping strategies
- Adapt recommendations to user's primary goal

Key principles:
- High stress + high intensity workouts = cortisol overload (bad)
- Moderate stress + moderate exercise = stress relief (good)
- Chronic stress = prioritize recovery and restoration
- Breathing exercises are powerful for acute stress
- Sleep and stress are deeply connected

Stress-Exercise Guidelines:
- LOW stress: Normal workout intensity fine
- MODERATE stress: Moderate exercise helps (avoid max intensity)
- HIGH stress: Light movement only (walks, gentle yoga, stretching)
- CHRONIC stress: Focus on restorative practices, reduce workout volume

Respond with JSON:
{
    "recommendation": "Specific action to take (be concrete)",
    "rationale": "Why this helps based on stress physiology",
    "avoid": ["What NOT to do given stress level"],
    "alternatives": ["Other options if recommendation doesn't work"],
    "breathing_exercises": ["Specific techniques for acute stress"],
    "confidence": 0.85
}

Examples:
- High stress + planned HIIT → "Replace HIIT with 20-min walk. High cortisol + intense exercise = injury risk and burnout."
- Moderate stress + rest day → "Light yoga or stretching. Movement helps stress, but keep it gentle."
- Chronic stress + heavy lifting → "Reduce volume 40%, add meditation. Your body needs recovery, not more stress."
"""
    
    def _build_user_prompt(
        self,
        stress_level: str,
        stress_source: str,
        current_activities: list,
        primary_goal: str,
        context: Dict[str, Any]
    ) -> str:
        """Build user prompt with stress context"""
        
        activities_text = ", ".join(current_activities) if current_activities else "None planned"
        
        return f"""Recommend stress management intervention:

STRESS LEVEL: {stress_level}
STRESS SOURCE: {stress_source}

PRIMARY GOAL: {primary_goal}

CURRENT ACTIVITIES PLANNED: {activities_text}

CONTEXT:
- Sleep: {context.get('sleep_hours', 'unknown')}h last night
- Energy: {context.get('energy_level', 'unknown')}
- Days since last workout: {context.get('days_since_last_workout', 'unknown')}

Your task:
1. Assess if current activities are appropriate given stress level
2. Recommend specific intervention (modify, replace, or add activities)
3. Provide rationale based on stress physiology
4. Suggest breathing exercises for acute stress moments

Generate the JSON response."""


# Singleton instance
stress_management_agent = StressManagementAgent()
