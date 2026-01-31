"""Biometric Agent - Analyzes sleep, HRV, recovery"""
from typing import Dict, Any
from agents.base_agent import BaseAgent

class BiometricAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Biometric Agent",
            description="Analyzes sleep and recovery data",
            model="llama-3.3-70b-versatile"
        )
    
    async def analyze(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze daily check-in data to determine readiness.
        """
        checkin_data = input_data.get("checkin_data", {})
        recent_workouts = input_data.get("recent_workouts", [])
        user_profile = input_data.get("user_profile", {})
        user_memory = input_data.get("user_memory", {})
        
        # Build context from memory
        memory_context = ""
        if user_memory:
            biometric_learnings = user_memory.get("by_type", {}).get("biometric_baseline", [])
            if biometric_learnings:
                memory_context = "\nUSER BASELINE (from memory):\n" + "\n".join(
                    [f"- {l['content'].get('insight', '')}" for l in biometric_learnings[:3]]
                )

        system_prompt = """You are an expert physiologist analyzing user self-reported check-in data.
        
        Your goal:
        - Determine "Readiness Score" (0.0 - 1.0) based on subjective feedback
        - Identify recovery deficits
        - Suggest immediate adjustments
        
        Input Mappings:
        - Sleep Quality (1-5): 1=Terrible, 5=Amazing
        - Energy (energized/normal/tired/exhausted)
        - Soreness (none/mild/moderate/significant)
        - Stress (low/moderate/high/overwhelming)
        
        Scoring Logic:
        - Sleep 1-2 OR Exhausted OR Significant Soreness = Low Readiness (<0.5)
        - Sleep 3 + Normal Energy = Moderate Readiness (0.5-0.7)
        - Sleep 4-5 + Energized = High Readiness (>0.8)
        - High Stress = Reduce intensity regardless of physical state
        
        Respond with JSON:
        {
            "analysis": {
                "sleep_quality_rating": 4,
                "energy_status": "normal",
                "readiness": 0.75,
                "recovery_status": "recovered|strained|under_recovered"
            },
            "stress_score": 0.3,
            "insights": ["Sleep was good but stress is moderate"],
            "recommendations": ["Maintain volume, monitor stress"],
            "confidence": 0.9
        }"""
        
        user_prompt = f"""
        Daily Check-In Data:
        - Sleep Quality: {checkin_data.get('sleep_quality', 'unknown')}/5
        - Energy Level: {checkin_data.get('energy_level', 'unknown')}
        - Soreness: {checkin_data.get('soreness_level', 'unknown')}
        - Stress Level: {checkin_data.get('stress_level', 'unknown')}
        - Notes: {checkin_data.get('notes', 'none')}
        
        Recent Workouts: {len(recent_workouts)} in last 7 days
        User Profile: {user_profile.get('fitness_level', 'unknown')}
        {memory_context}
        
        Analyze readiness and recovery status.
        """
        
        response = await self._call_llm(system_prompt, user_prompt)
        analysis = self._parse_json_response(response)
        
        return analysis