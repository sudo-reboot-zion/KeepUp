from typing import Dict, Any
from agents.base_agent import BaseAgent

class DrillSergeantAgent(BaseAgent):
    """
    Focuses on intensity, progression, and breaking plateaus.
    """
    def __init__(self):
        super().__init__(
            name="Drill Sergeant Agent",
            description="Focuses on maximizing performance, intensity, and progressive overload.",
            model="llama-3.3-70b-versatile"
        )

    async def analyze(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        user_profile = input_data.get("user_profile", {})
        workout_plan = input_data.get("workout_plan", [])
        context = input_data.get("context", {})

        system_prompt = """You are the Drill Sergeant. Your goal is to push the user to their limits (safely).
        You believe in progressive overload and that comfort is the enemy of progress.
        Review the workout and suggest ways to increase intensity, volume, or density.
        
        Response JSON:
        {
            "critique": "The workout is too easy...",
            "modifications": [
                {"exercise": "Squats", "change": "Increase weight by 5%", "reason": "User is ready"}
            ],
            "intensity_score": 0.9
        }
        """
        
        user_prompt = f"""
        User: {user_profile.get('fitness_level')}
        Context: {context}
        Workout: {workout_plan}
        
        How can we make this harder and more effective?
        """

        response = await self._call_llm(system_prompt, user_prompt)
        return self._parse_json_response(response)

drill_sergeant_agent = DrillSergeantAgent()
