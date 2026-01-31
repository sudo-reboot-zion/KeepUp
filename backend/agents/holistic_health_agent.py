"""
Holistic Health Agent
Analyzes cross-dimension impacts and recommends focus shifts.
"""
from typing import Dict, Any, List
from agents.base_agent import BaseAgent

class HolisticHealthAgent(BaseAgent):
    """
    The Guardian of Balance - Monitors all health dimensions to prevent tunnel vision.
    
    Responsibilities:
    - Analyze how supporting dimensions (sleep, stress, etc.) impact the primary goal
    - Detect when a supporting dimension becomes critical (e.g., sleep debt > 10h)
    - Recommend temporary focus shifts (e.g., "Shift to Sleep Focus for 3 days")
    - Calculate overall Health Balance Score
    """
    
    def __init__(self):
        super().__init__(
            name="Holistic Health Agent",
            description="Analyzes cross-dimension impacts and ensures holistic balance",
            model="llama-3.3-70b-versatile"
        )
    
    async def analyze(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze holistic health state.
        
        Input:
            - primary_goal: str
            - biometrics: Dict (sleep, stress, activity, etc.)
            - recent_history: List[Dict] (last 7 days)
            
        Returns:
            - health_balance_score: float (0-100)
            - dimension_scores: Dict[str, float]
            - critical_alerts: List[str]
            - focus_shift_recommendation: Optional[Dict]
        """
        primary_goal = input_data.get("primary_goal", "wellness")
        biometrics = input_data.get("biometrics", {})
        
        system_prompt = self._build_system_prompt(primary_goal)
        user_prompt = self._build_user_prompt(biometrics, primary_goal)
        
        response = await self._call_llm(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.3,
            max_tokens=1000
        )
        
        return self._parse_json_response(response)
    
    def _build_system_prompt(self, primary_goal: str) -> str:
        return f"""You are the Holistic Health Agent.
        
Your role is to ensure the user doesn't sacrifice overall health while pursuing their PRIMARY GOAL: {primary_goal.upper()}.

You analyze 4 dimensions:
1. Sleep (Quantity & Quality)
2. Stress (Mental & Physical)
3. Activity (Movement & Recovery)
4. Nutrition (Fuel & Hydration)

Logic for {primary_goal.upper()} users:
- If a supporting dimension drops below critical threshold, you MUST trigger a "Focus Shift".
- Example: If a Fitness user has 3 nights of poor sleep, recommend shifting to Sleep Focus.
- Example: If a Career/Stress user has high physical exhaustion, recommend shifting to Recovery Focus.

Respond with JSON:
{{
    "health_balance_score": 85,  // 0-100 overall score
    "dimension_status": {{
        "sleep": "optimal|good|fair|poor|critical",
        "stress": "low|moderate|high|critical",
        "activity": "optimal|good|fair|poor|critical",
        "nutrition": "optimal|good|fair|poor|critical"
    }},
    "cross_impact_analysis": "Explanation of how dimensions are affecting each other (e.g., 'High stress is ruining sleep quality')",
    "critical_alerts": ["List of urgent issues"],
    "focus_shift_recommendation": {{
        "should_shift": boolean,
        "target_focus": "fitness|sleep|stress|wellness|recovery",
        "duration_days": 1-7,
        "reason": "Why the shift is needed"
    }}
}}"""

    def _build_user_prompt(self, biometrics: Dict[str, Any], primary_goal: str) -> str:
        return f"""Analyze this user's state:
        
Primary Goal: {primary_goal}

Biometrics:
- Sleep Quality: {biometrics.get('sleep_quality', 'unknown')}/5
- Sleep Hours: {biometrics.get('sleep_hours', 'unknown')}
- Stress Level: {biometrics.get('stress_level', 'unknown')}
- Energy Level: {biometrics.get('energy_level', 'unknown')}
- Soreness: {biometrics.get('soreness_level', 'unknown')}
- Readiness: {biometrics.get('readiness_score', 'unknown')}

Determine if a focus shift is needed to protect long-term progress."""
