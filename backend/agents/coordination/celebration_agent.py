"""
Celebration Agent
The Hype Man. Celebrates wins, big and small.
"""
from typing import Dict, Any
from agents.base_agent import BaseAgent

class CelebrationAgent(BaseAgent):
    """
    The Hype Man.
    
    Responsibilities:
    1. Detect milestones (Challenge complete, 7-day streak, PR).
    2. Send "Kudos" notifications.
    3. Generate "Badge" unlock messages.
    """
    
    def __init__(self):
        super().__init__(
            name="Celebration Agent",
            description="Celebrates user achievements and milestones",
            model="llama-3.3-70b-versatile"
        )
    
    async def celebrate_milestone(self, milestone_type: str, details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a celebration message.
        """
        system_prompt = """You are the Celebration Agent (The Hype Man).
        
        Your Goal: Make the user feel like a champion.
        Tone: Energetic, sincere, exciting (but not cringe).
        
        Input: Milestone details.
        Output: A short, punchy notification message.
        
        Respond with JSON:
        {
            "title": "🎉 Challenge Crushed!",
            "body": "You just finished the 7-Day Sleep Sprint! That's huge!",
            "badge_unlocked": "Sleep Warrior"
        }"""
        
        user_prompt = f"Milestone: {milestone_type}\nDetails: {details}"
        
        response = await self._call_llm(system_prompt, user_prompt)
        return self._parse_json_response(response)

    async def analyze(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze potential celebrations.
        """
        action = input_data.get("action")
        
        if action == "celebrate":
            milestone_type = input_data.get("milestone_type", "generic")
            details = input_data.get("details", {})
            return await self.celebrate_milestone(milestone_type, details)
            
        return {"error": "Unknown action", "input": input_data}

celebration_agent = CelebrationAgent()
