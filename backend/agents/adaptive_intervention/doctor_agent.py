from typing import Dict, Any
from agents.base_agent import BaseAgent

class DoctorAgent(BaseAgent):
    """
    Focuses on safety, recovery, and longevity.
    """
    def __init__(self):
        super().__init__(
            name="Doctor Agent",
            description="Focuses on injury prevention, recovery, and long-term health.",
            model="llama-3.3-70b-versatile"
        )

    async def analyze(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        user_profile = input_data.get("user_profile", {})
        workout_plan = input_data.get("workout_plan", [])
        context = input_data.get("context", {})

        system_prompt = """You are the Doctor. Your goal is to ensure the user exercises safely and recovers well.
        You prioritize longevity over short-term gains.
        Review the workout and suggest ways to reduce risk, improve form, or enhance recovery.
        
        Response JSON:
        {
            "critique": "The volume is too high for the reported sleep...",
            "modifications": [
                {"exercise": "Deadlifts", "change": "Reduce sets to 2", "reason": "Lower back fatigue risk"}
            ],
            "safety_score": 0.95
        }
        """
        
        user_prompt = f"""
        User: {user_profile.get('fitness_level')}
        Context: {context}
        Workout: {workout_plan}
        
        How can we make this safer and more sustainable?
        """

        response = await self._call_llm(system_prompt, user_prompt)
        return self._parse_json_response(response)

doctor_agent = DoctorAgent()
