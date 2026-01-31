"""
Meditation Agent
Recommends meditation/mindfulness for stress and mental performance
"""
from typing import Dict, Any
from agents.base_agent import BaseAgent
from agents.constraint_framework import INDIVIDUAL_AGENT_PROMPT


class MeditationAgent(BaseAgent):
    """
    Recommends meditation and mindfulness practices
    
    Responsibilities:
    - Detect when stress is hurting performance
    - Recommend specific meditation practices
    - Integrate mindfulness into workout routine
    - Build mental resilience
    """
    
    def __init__(self):
        super().__init__(
            name="Meditation Agent",
            description="Mindfulness expert who builds mental resilience and manages stress",
            model="llama-3.3-70b-versatile"
        )
    
    async def analyze(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recommend meditation interventions
        
        Input:
            - stress_score: float
            - motivation_state: str
            - barriers: List[str]
            - user_profile: Dict
            
        Returns:
            - recommendation: Dict
            - practices: List[Dict]
            - integration_strategy: str
            - confidence: float
        """
        
        stress_score = input_data.get("stress_score", 0.5)
        motivation_state = input_data.get("motivation_state", "moderate")
        barriers = input_data.get("barriers", [])
        user_profile = input_data.get("user_profile", {})
        
        constraint_prompt = INDIVIDUAL_AGENT_PROMPT.format(
            agent_name="Meditation Agent",
            specialty="recommending mindfulness practices to manage stress and improve performance"
        )
        system_prompt = constraint_prompt + "\n" + """You are a mindfulness and meditation expert specializing in athletic performance.

Your role:
- Recommend meditation when stress is high
- Provide practical, time-efficient practices
- Integrate mindfulness into existing routines
- Build mental resilience gradually

Meditation practices:
- Box Breathing: 4-4-4-4, great for immediate stress relief
- Body Scan: 5-10min, improves mind-muscle connection
- Visualization: 5min pre-workout, enhances performance
- Gratitude Practice: 2min, boosts motivation
- Walking Meditation: Active mindfulness

Respond with JSON:
{
    "recommendation": {
        "primary_practice": "Box Breathing",
        "duration": "5 minutes",
        "timing": "Morning or pre-workout",
        "rationale": "Immediate stress relief, easy to start"
    },
    "practices": [
        {
            "name": "Box Breathing",
            "instructions": "Inhale 4, hold 4, exhale 4, hold 4. Repeat 10 cycles",
            "when": "When feeling stressed or before workout",
            "benefits": ["Reduces cortisol", "Improves focus", "Calms nervous system"]
        }
    ],
    "integration_strategy": "Start with 5min/day, add to morning routine",
    "expected_benefits": ["Better stress management", "Improved workout focus"],
    "confidence": 0.80
}"""
        
        user_prompt = f"""Recommend meditation practices:

CURRENT STATE:
- Stress Score: {stress_score} (0-1 scale)
- Motivation: {motivation_state}
- Barriers: {', '.join(barriers) if barriers else 'None'}

USER PROFILE:
- Experience with Meditation: {user_profile.get('meditation_experience', 'none')}
- Available Time: {user_profile.get('available_time', '10-15 minutes')}
- Preferences: {user_profile.get('preferences', 'unknown')}

Your task:
1. Recommend appropriate practice for stress level
2. Provide clear, simple instructions
3. Integrate into existing routine
4. Start small and sustainable

Generate JSON response."""
        
        response = await self._call_llm(system_prompt, user_prompt, temperature=0.3, max_tokens=1200)
        return self._parse_json_response(response)


# Singleton instance
meditation_agent = MeditationAgent()