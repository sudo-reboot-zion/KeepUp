# agents/contextual_awareness/barrier_detection_agent.py
"""
Barrier Detection Agent - Identifies obstacles preventing workout completion
"""
from typing import Dict, Any
from agents.base_agent import BaseAgent


class BarrierDetectionAgent(BaseAgent):
    """Detects barriers preventing user from working out"""
    
    def __init__(self):
        super().__init__(
            name="Barrier Detection Agent",
            description="Identifies specific obstacles preventing workout completion",
            model="llama-3.3-70b-versatile"
        )
    
    async def analyze(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect barriers from patterns
        
        Common barriers:
        - Time constraints
        - Fatigue/burnout
        - Lack of motivation
        - Environmental factors
        - Social obligations
        - Monotony/boredom
        """
        
        system_prompt = """You are an expert at identifying barriers to behavior change.

Analyze the user's situation and identify specific barriers preventing workouts.

Common barrier categories:
- TIME: Schedule conflicts, time pressure
- ENERGY: Fatigue, poor sleep, burnout
- MOTIVATION: Loss of interest, lack of purpose
- ENVIRONMENT: Gym access, weather, space
- SOCIAL: Family obligations, peer pressure
- PSYCHOLOGICAL: Perfectionism, fear of failure

Respond with JSON:
{
    "barriers": ["specific barrier 1", "barrier 2"],
    "categories": ["TIME", "MOTIVATION"],
    "primary_barrier": "most likely culprit",
    "severity": 0.75,
    "confidence": 0.80
}"""
        
        user_prompt = f"""User Context:
{input_data}

What barriers are preventing this user from working out?"""
        
        response = await self._call_llm(system_prompt, user_prompt)
        return self._parse_json_response(response)


# agents/contextual_awareness/motivation_agent.py
"""
Motivation Agent - Assesses psychological state
"""
from typing import Dict, Any
from agents.base_agent import BaseAgent


class MotivationAgent(BaseAgent):
    """Assesses user's motivational state"""
    
    def __init__(self):
        super().__init__(
            name="Motivation Agent",
            description="Assesses psychological and motivational state",
            model="llama-3.3-70b-versatile"
        )
    
    async def analyze(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess motivational state
        
        States:
        - HIGH: Enthusiastic, consistent
        - MODERATE: Doing it but not loving it
        - LOW: Dragging themselves
        - DEPLETED: Burnout, considering quitting
        """
        
        system_prompt = """You are a behavioral psychologist specializing in motivation.

Assess the user's motivational state based on their behavior patterns.

Motivational states:
- HIGH: Enthusiastic, self-motivated, consistent
- MODERATE: Still going but requires effort
- LOW: Struggling, needs external motivation
- DEPLETED: Burnout, considering quitting

Respond with JSON:
{
    "state": "HIGH|MODERATE|LOW|DEPLETED",
    "motivation_drop": true,
    "indicators": ["what suggests this state"],
    "intervention_urgency": "low|medium|high",
    "recommended_approach": "encouragement|reduction|pause",
    "confidence": 0.75
}"""
        
        user_prompt = f"""User Context:
{input_data}

What is this user's motivational state?"""
        
        response = await self._call_llm(system_prompt, user_prompt)
        return self._parse_json_response(response)


motivation_agent = MotivationAgent()
