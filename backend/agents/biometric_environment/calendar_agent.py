"""Calendar Agent - Checks schedule conflicts"""
from typing import Dict, Any
from agents.base_agent import BaseAgent

class CalendarAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Calendar Agent",
            description="Analyzes calendar for workout timing",
            model="llama-3.1-70b-versatile"
        )
    
    async def analyze(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Placeholder - returns no conflicts"""
        return {
            "conflicts": []
        }