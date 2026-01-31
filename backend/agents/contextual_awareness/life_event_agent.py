"""
Life Event Agent
Detects major life events that might impact fitness adherence
"""
from typing import Dict, Any
from agents.base_agent import BaseAgent


class LifeEventAgent(BaseAgent):
    """
    Detects life events (travel, job change, moving, etc.) that affect workouts
    
    Responsibilities:
    - Identify disruptive life events
    - Predict impact on adherence
    - Suggest adaptations
    """
    
    def __init__(self):
        super().__init__(
            name="Life Event Agent",
            description="Detects life events and their impact on fitness routine",
            model="llama-3.3-70b-versatile"
        )
    
    async def analyze(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect life events from calendar and user notes
        
        Input:
            - calendar_events: List[Dict]
            - user_notes: str
            - adherence_pattern: List
            - detected_barriers: List
            
        Returns:
            - life_events: List[Dict]
            - impact_assessment: Dict
            - adaptation_suggestions: List
            - confidence: float
        """
        
        calendar_events = input_data.get("calendar_events", [])
        user_notes = input_data.get("user_notes", "")
        adherence_pattern = input_data.get("adherence_pattern", [])
        
        # Simple detection logic
        life_events = []
        
        # Check calendar for travel
        for event in calendar_events:
            title = event.get("title", "").lower()
            if any(keyword in title for keyword in ["travel", "trip", "vacation", "conference"]):
                life_events.append({
                    "type": "travel",
                    "description": event.get("title"),
                    "impact": "high",
                    "dates": event.get("dates", [])
                })
        
        # Check for job-related events
        if any(keyword in user_notes.lower() for keyword in ["new job", "started work", "promotion"]):
            life_events.append({
                "type": "job_change",
                "description": "Career transition detected",
                "impact": "medium"
            })
        
        return {
            "life_events": life_events,
            "impact_assessment": {
                "severity": "high" if len(life_events) > 0 else "low",
                "affected_weeks": len(life_events) * 2
            },
            "adaptation_suggestions": [
                "Reduce workout frequency during transition",
                "Focus on bodyweight exercises while traveling"
            ] if life_events else [],
            "confidence": 0.7,
            "agent_name": self.name
        }


# Singleton instance
life_event_agent = LifeEventAgent()
