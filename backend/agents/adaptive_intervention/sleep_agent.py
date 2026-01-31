from typing import Dict, Any
import time
from ..base_agent import BaseAgent


class SleepAgent(BaseAgent):

    """
    Analyzes sleep quality and provides recovery recommendations.
    """

    def __init__(self):
        super().__init__(
            name="Sleep Agent",
            description="Analyzes Sleep quality and impact on training capacity",
            model="llama-3.1-70b-versatile"
        )

    async def analyze(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main analysis method
        """

        start_time = time.time()

        hours_slept = input_data.get("hours_slept", 0)
        sleep_quality = input_data.get("sleep_quality", 5)
        user_baseline = input_data.get("user_baseline", 7.5)
        sleep_debt = input_data.get("sleep_debt_accumulated", 0)

        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(
            hours_slept,
            sleep_quality,
            user_baseline,
            sleep_debt
        )

        llm_response = await self._call_llm(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.2
        )

        analysis = self._parse_json_response(llm_response)

        execution_time = time.time() - start_time
        
        return {
            "analysis": analysis,
            "execution_time": execution_time
        }

    def _build_system_prompt(self) -> str:
        return """You are an expert Sleep Scientist and Recovery Specialist.
        
        Your goal is to analyze the user's sleep data and determine:
        1. Their current recovery state (0-100%)
        2. Impact on cognitive and physical performance
        3. Specific actionable recommendations to improve sleep tonight
        4. Whether they need a "Sleep Intervention" (drastic change to schedule)

        Respond in JSON format:
        {
            "recovery_score": 85,
            "state": "Well Rested",
            "impact": "High readiness for physical training",
            "recommendation": "Maintain current routine",
            "intervention_needed": false
        }
        """

    def _build_user_prompt(self, hours, quality, baseline, debt) -> str:
        return f"""Analyze this sleep data:
        - Hours Slept: {hours} (Baseline: {baseline})
        - Quality: {quality}/5
        - Accumulated Debt: {debt} hours
        
        Provide recovery analysis."""

# Singleton instance
sleep_agent = SleepAgent()