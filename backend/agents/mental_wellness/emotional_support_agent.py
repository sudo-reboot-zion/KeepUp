"""
Emotional Support Agent
Provides encouragement, celebrates wins, reframes negative thinking
"""
from typing import Dict, Any
from agents.base_agent import BaseAgent
from agents.constraint_framework import INDIVIDUAL_AGENT_PROMPT


class EmotionalSupportAgent(BaseAgent):
    """
    Provides emotional support, encouragement, and cognitive reframing
    
    Responsibilities:
    - Celebrate victories (scale and non-scale)
    - Reframe negative self-talk
    - Provide empathy during setbacks
    - Maintain motivation through tough periods
    - Recognize effort, not just results
    """
    
    def __init__(self):
        super().__init__(
            name="Emotional Support Agent",
            description="Provides encouragement, celebrates wins, and reframes negative thinking",
            model="llama-3.3-70b-versatile"
        )
    
    async def analyze(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Provide emotional support based on user's current state
        
        Input:
            - user_state: str (struggling, neutral, celebrating)
            - recent_events: List[str] (what happened recently)
            - self_talk: str (user's internal narrative)
            - progress_context: Dict (overall progress)
            - primary_goal: str (fitness, sleep, stress, wellness)
            
        Returns:
            - support_message: str
            - reframing: str (if negative self-talk detected)
            - celebration: str (if wins detected)
            - confidence: float
        """
        
        # Extract inputs
        user_state = input_data.get("user_state", "neutral")
        recent_events = input_data.get("recent_events", [])
        self_talk = input_data.get("self_talk", "")
        progress_context = input_data.get("progress_context", {})
        primary_goal = input_data.get("primary_goal", "wellness")
        user_memory = input_data.get("user_memory", {})
        
        # Build prompts
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(
            user_state, recent_events, self_talk, progress_context, primary_goal, user_memory
        )
        
        # Call LLM
        response = await self._call_llm(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.7,  # Higher for more empathetic, varied responses
            max_tokens=800
        )
        
        result = self._parse_json_response(response)
        
        return {
            "support_message": result.get("support_message", ""),
            "reframing": result.get("reframing", ""),
            "celebration": result.get("celebration", ""),
            "encouragement_type": result.get("encouragement_type", "general"),
            "confidence": result.get("confidence", 0.0),
            "agent_name": self.name
        }
    
    def _build_system_prompt(self) -> str:
        """Build system prompt for emotional support"""
        constraint_prompt = INDIVIDUAL_AGENT_PROMPT.format(
            agent_name="Emotional Support Agent",
            specialty="providing empathetic encouragement and cognitive reframing for health goals"
        )
        return constraint_prompt + """

You are a compassionate wellness coach specializing in emotional support and motivation.

Your role:
- Celebrate ALL wins (scale and non-scale victories)
- Reframe negative self-talk with compassion
- Provide empathy during setbacks
- Recognize effort and process, not just outcomes
- Maintain realistic optimism

Key principles:
- NEVER toxic positivity ("just be positive!")
- Acknowledge struggle while highlighting resilience
- Celebrate non-scale victories (better sleep, more energy, consistency)
- Reframe "failure" as "data" or "learning"
- Remind users: health is a journey, not a destination

Respond with JSON:
{
    "support_message": "Main encouraging message tailored to their state",
    "reframing": "If negative self-talk detected, reframe it compassionately",
    "celebration": "If wins detected, celebrate them specifically",
    "encouragement_type": "empathy|celebration|reframing|motivation",
    "confidence": 0.85
}

Examples of good reframing:
- "I'm a failure" → "You showed up 3 days this week. That's 3 more than if you'd quit."
- "I'll never lose weight" → "Weight fluctuates daily. Your energy is up and sleep improved—those matter too."
- "I missed my workout" → "One missed workout doesn't erase your consistency. What can we learn from this?"
"""
    
    def _build_user_prompt(
        self,
        user_state: str,
        recent_events: list,
        self_talk: str,
        progress_context: Dict[str, Any],
        primary_goal: str,
        user_memory: Dict[str, Any]
    ) -> str:
        """Build user prompt with emotional context"""
        
        events_text = "\n".join([f"- {event}" for event in recent_events]) if recent_events else "No recent events logged"
        
        # Format memory for context
        memory_context = ""
        if user_memory:
            past_struggles = user_memory.get("by_type", {}).get("failure_pattern", [])
            if past_struggles:
                memory_context = "\n\nPAST STRUGGLES (be sensitive):\n" + "\n".join(
                    [f"- {s['content'].get('pattern', '')}" for s in past_struggles[:2]]
                )
        
        return f"""Provide emotional support for this user:

USER STATE: {user_state}

PRIMARY GOAL: {primary_goal}

RECENT EVENTS:
{events_text}

USER'S SELF-TALK: "{self_talk}"

PROGRESS CONTEXT:
- Adherence: {progress_context.get('adherence_rate', 'unknown')}
- Trend: {progress_context.get('trend', 'unknown')}
- Wins: {', '.join(progress_context.get('wins', [])) or 'None logged'}
{memory_context}

Your task:
1. Acknowledge their current state with empathy
2. If self-talk is negative, reframe it compassionately
3. Celebrate any wins (even small ones)
4. Provide encouragement tailored to their primary goal
5. Be genuine, not robotic

Generate the JSON response."""
    


# Singleton instance
emotional_support_agent = EmotionalSupportAgent()
