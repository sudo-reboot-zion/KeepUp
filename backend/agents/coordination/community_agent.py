"""
Community Agent
Fosters engagement through shared challenges and "Pulse" updates.
"""
from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from datetime import datetime, timedelta

class CommunityAgent(BaseAgent):
    """
    The Community Manager.
    
    Responsibilities:
    1. Generate Weekly Challenges based on user goals (Tribes).
    2. Summarize community activity ("The Pulse").
    3. Normalize failure ("78% of people struggle with Day 3").
    """
    
    def __init__(self):
        super().__init__(
            name="Community Agent",
            description="Fosters community engagement through challenges and encouragement",
            model="llama-3.3-70b-versatile"
        )
    
    async def generate_challenge(self, tribe_goal: str, active_users_count: int) -> Dict[str, Any]:
        """
        Generate a new weekly challenge for a specific tribe (e.g., "Sleep Tribe").
        """
        system_prompt = f"""You are the Community Manager for the {tribe_goal.upper()} Tribe.
        
        Your Goal: Create a 7-day challenge that is:
        1. Achievable (target 75% completion)
        2. Social (fun to do together)
        3. Simple (one tap to join)
        
        Context:
        - Tribe: {tribe_goal} (e.g., Fitness, Sleep, Stress)
        - Active Members: {active_users_count}
        
        Respond with JSON:
        {{
            "title": "The 7-Day Sleep Hygiene Sprint",
            "description": "Turn off screens 30m before bed for 7 days straight.",
            "difficulty": "beginner",
            "daily_actions": ["No phone after 10pm", "Read a book", ...],
            "encouragement": "Join {active_users_count} others in reclaiming your rest!"
        }}"""
        
        response = await self._call_llm(system_prompt, "Generate this week's challenge.")
        return self._parse_json_response(response)

    async def generate_pulse_update(self, recent_activities: List[Dict]) -> str:
        """
        Generate a "Pulse" update string for the dashboard.
        "🔥 12 people just finished Day 3! Sarah hit a PR!"
        """
        # Simplified logic for MVP
        count = len(recent_activities)
        if count == 0:
            return "The community is quiet... be the first to move!"
            
        return f"🔥 {count} members are active right now! Keep pushing!"

    async def analyze(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze community data or requests.
        """
        action = input_data.get("action")
        
        if action == "generate_challenge":
            tribe = input_data.get("tribe", "general")
            count = input_data.get("active_users_count", 100)
            return await self.generate_challenge(tribe, count)
            
        elif action == "generate_pulse":
            activities = input_data.get("recent_activities", [])
            pulse = await self.generate_pulse_update(activities)
            return {"pulse_text": pulse}
            
        return {"error": "Unknown action", "input": input_data}

community_agent = CommunityAgent()
