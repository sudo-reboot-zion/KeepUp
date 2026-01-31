"""
Chat Agent
Conversational interface for onboarding and daily check-ins
"""
from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from agents.constraint_framework import INDIVIDUAL_AGENT_PROMPT


class ChatAgent(BaseAgent):
    """
    Conversational interface for onboarding and daily interactions
    
    Responsibilities:
    - Conduct natural onboarding conversation
    - Determine user's primary goal (fitness, sleep, stress, wellness)
    - Extract key context (occupation, constraints, past attempts)
    - Daily check-ins and progress conversations
    - Natural language interaction
    """
    
    def __init__(self):
        super().__init__(
            name="Chat Agent",
            description="Conversational interface for onboarding and daily check-ins",
            model="llama-3.3-70b-versatile"
        )
        self.history: Dict[str, List[Dict[str, Any]]] = {}

    async def respond(self, user_id: str, message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        High-level method to handle a user message and return a response.
        Matches the interface expected by api/routes/chat.py
        """
        # Get history
        user_history = self._get_conversation_history(user_id)
        
        # Add user message to history
        user_history.append({"role": "user", "content": message})
        
        # Analyze using current state
        # In a real RAG system, we might fetch more context here
        input_data = {
            "conversation_history": user_history,
            "user_message": message,
            "conversation_stage": context.get("stage", "general") if context else "general",
            "extracted_data": context.get("extracted_data", {}) if context else {}
        }
        
        result = await self.analyze(input_data)
        
        # Add agent response to history
        user_history.append({"role": "assistant", "content": result["agent_response"]})
        
        # Truncate history if too long (keep last 20)
        self.history[user_id] = user_history[-20:]
        
        return {
            "message": result["agent_response"],
            "data": result.get("extracted_info", {}),
            "actions": [], # Can be expanded for UI actions
            "confidence": result.get("confidence", 0.8)
        }

    def _get_conversation_history(self, user_id: str) -> List[Dict[str, Any]]:
        """Get history for a specific user"""
        if user_id not in self.history:
            self.history[user_id] = []
        return self.history[user_id]

    def clear_history(self, user_id: str):
        """Clear history for a specific user"""
        if user_id in self.history:
            self.history[user_id] = []
    
    async def analyze(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process conversation and extract structured information
        
        Input:
            - conversation_history: List[Dict] (previous messages)
            - user_message: str (latest user message)
            - conversation_stage: str (onboarding, daily_checkin, goal_clarification)
            - extracted_data: Dict (data extracted so far)
            
        Returns:
            - agent_response: str (what to say to user)
            - extracted_info: Dict (structured data extracted)
            - next_question: str (what to ask next, if needed)
            - conversation_complete: bool
            - confidence: float
        """
        
        # Extract inputs
        conversation_history = input_data.get("conversation_history", [])
        user_message = input_data.get("user_message", "")
        stage = input_data.get("conversation_stage", "onboarding")
        extracted_data = input_data.get("extracted_data", {})
        
        # NEW: Get user's primary goal for context
        user_profile = input_data.get("user_profile", {})
        primary_goal = user_profile.get("primary_goal", "wellness")
        
        # Route to appropriate conversation handler
        if stage == "onboarding":
            return await self._handle_onboarding(
                conversation_history, user_message, extracted_data
            )
        elif stage == "daily_checkin":
            return await self._handle_daily_checkin(
                conversation_history, user_message, extracted_data, primary_goal
            )
        elif stage == "evening_checkin":
            return await self._handle_evening_checkin(
                conversation_history, user_message, extracted_data, primary_goal
            )
        else:
            return await self._handle_general_conversation(
                conversation_history, user_message, extracted_data
            )
    
    async def _handle_onboarding(
        self,
        conversation_history: List[Dict],
        user_message: str,
        extracted_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle onboarding conversation"""
        
        system_prompt = self._build_onboarding_system_prompt()
        user_prompt = self._build_onboarding_user_prompt(
            conversation_history, user_message, extracted_data
        )
        
        response = await self._call_llm(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.6,
            max_tokens=1000
        )
        
        result = self._parse_json_response(response)
        
        return {
            "agent_response": result.get("agent_response", ""),
            "extracted_info": result.get("extracted_info", {}),
            "next_question": result.get("next_question", ""),
            "conversation_complete": result.get("conversation_complete", False),
            "confidence": result.get("confidence", 0.0),
            "agent_name": self.name
        }
    
    async def _handle_daily_checkin(
        self,
        conversation_history: List[Dict],
        user_message: str,
        extracted_data: Dict[str, Any],
        primary_goal: str = "wellness"
    ) -> Dict[str, Any]:
        """Handle daily check-in conversation"""
        
        system_prompt = self._build_daily_checkin_system_prompt(primary_goal)
        user_prompt = self._build_daily_checkin_user_prompt(
            conversation_history, user_message, extracted_data
        )
        
        response = await self._call_llm(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.6,
            max_tokens=800
        )
        
        result = self._parse_json_response(response)
        
        return {
            "agent_response": result.get("agent_response", ""),
            "extracted_info": result.get("extracted_info", {}),
            "conversation_complete": result.get("conversation_complete", False),
            "confidence": result.get("confidence", 0.0),
            "agent_name": self.name
        }

    async def _handle_evening_checkin(
        self,
        conversation_history: List[Dict],
        user_message: str,
        extracted_data: Dict[str, Any],
        primary_goal: str = "wellness"
    ) -> Dict[str, Any]:
        """Handle evening check-in conversation"""
        
        system_prompt = self._build_evening_checkin_system_prompt(primary_goal)
        user_prompt = self._build_daily_checkin_user_prompt(
            conversation_history, user_message, extracted_data
        )
        
        response = await self._call_llm(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.6,
            max_tokens=800
        )
        
        result = self._parse_json_response(response)
        
        return {
            "agent_response": result.get("agent_response", ""),
            "extracted_info": result.get("extracted_info", {}),
            "conversation_complete": result.get("conversation_complete", False),
            "confidence": result.get("confidence", 0.0),
            "agent_name": self.name
        }
    
    async def _handle_general_conversation(
        self,
        conversation_history: List[Dict],
        user_message: str,
        extracted_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle general conversation"""
        
        system_prompt = """You are a friendly health and wellness assistant.
        
Respond naturally to the user's message while staying focused on health, fitness, and wellness.

Respond with JSON:
{
    "agent_response": "Your natural response to the user",
    "extracted_info": {},
    "conversation_complete": false,
    "confidence": 0.80
}"""
        
        user_prompt = f"""User said: "{user_message}"

Respond naturally and helpfully."""
        
        response = await self._call_llm(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.7,
            max_tokens=600
        )
        
        result = self._parse_json_response(response)
        
        return {
            "agent_response": result.get("agent_response", ""),
            "extracted_info": result.get("extracted_info", {}),
            "conversation_complete": result.get("conversation_complete", False),
            "confidence": result.get("confidence", 0.0),
            "agent_name": self.name
        }
    
    def _build_onboarding_system_prompt(self) -> str:
        """Build system prompt for onboarding"""
        constraint_prompt = INDIVIDUAL_AGENT_PROMPT.format(
            agent_name="Chat Agent",
            specialty="conducting natural onboarding conversations to understand user health goals"
        )
        return constraint_prompt + """

You are a friendly onboarding assistant for KEEP UP, a holistic health app.

Your goal: Have a natural 5-minute conversation to understand the user's PRIMARY HEALTH GOAL.

The 4 primary goals are:
1. **FITNESS** (weight loss, muscle gain, strength, running, etc.)
2. **SLEEP** (improve sleep quality, fix insomnia, better rest)
3. **STRESS/EMOTIONAL WELLNESS** (manage anxiety, reduce stress, mental health)
4. **GENERAL WELLNESS** (more energy, overall health, balanced lifestyle)

Conversation flow:
1. Start warm and welcoming
2. Ask about their main health goal (open-ended)
3. Clarify which of the 4 categories fits best
4. Ask about constraints (time, occupation, past attempts)
5. Confirm understanding and set expectations

Key principles:
- Keep it conversational, not interrogative
- Ask ONE question at a time
- Listen for clues about their primary goal
- Don't assume fitness is everyone's goal
- Be empathetic about past failures

Respond with JSON:
{
    "agent_response": "What you say to the user (natural, friendly)",
    "extracted_info": {
        "primary_goal": "fitness|sleep|stress|wellness|unknown",
        "specific_goal": "e.g., lose 20 lbs, sleep 7+ hours, manage work stress",
        "occupation": "if mentioned",
        "constraints": ["time", "access to gym", etc.],
        "past_attempts": "if mentioned"
    },
    "next_question": "What to ask next (if conversation not complete)",
    "conversation_complete": false,
    "confidence": 0.85
}

Set conversation_complete to true ONLY when you have:
- Primary goal clearly identified
- Specific goal understood
- Key constraints noted
"""
    
    def _build_onboarding_user_prompt(
        self,
        conversation_history: List[Dict],
        user_message: str,
        extracted_data: Dict[str, Any]
    ) -> str:
        """Build user prompt for onboarding"""
        
        history_text = ""
        if conversation_history:
            history_text = "CONVERSATION SO FAR:\n" + "\n".join([
                f"{'User' if msg.get('role') == 'user' else 'You'}: {msg.get('content')}"
                for msg in conversation_history[-5:]  # Last 5 messages
            ]) + "\n\n"
        
        extracted_text = ""
        if extracted_data:
            extracted_text = f"\nDATA EXTRACTED SO FAR:\n{extracted_data}\n"
        
        return f"""{history_text}USER'S LATEST MESSAGE: "{user_message}"
{extracted_text}
Your task:
1. Respond naturally to what they said
2. Extract any new information
3. Ask the next logical question (if needed)
4. Mark conversation_complete if you have enough info

Generate the JSON response."""
    
    def _build_daily_checkin_system_prompt(self, primary_goal: str = "wellness") -> str:
        """Build system prompt for daily check-ins, tailored to primary goal"""
        
        goal_focus = ""
        if primary_goal == "fitness":
            goal_focus = "- Readiness for workout\n- Muscle soreness/recovery\n- Nutrition compliance"
        elif primary_goal == "sleep":
            goal_focus = "- Sleep duration and quality (CRITICAL)\n- Energy levels upon waking\n- Caffeine/screen time yesterday"
        elif primary_goal == "stress":
            goal_focus = "- Current stress level (1-10)\n- Anxiety triggers today\n- Mood state"
        else:
            goal_focus = "- Overall energy\n- Balance across health dimensions\n- General well-being"

        return f"""You are conducting a quick daily check-in for a user with PRIMARY GOAL: {primary_goal.upper()}.

Your goal: Understand how the user is doing today, specifically regarding their {primary_goal} goal.

Ask about:
{goal_focus}
- Any barriers or challenges

Keep it brief (2-3 questions max). Be supportive but focused.

Respond with JSON:
{{
    "agent_response": "Your check-in message",
    "extracted_info": {{
        "energy_level": "low|moderate|high",
        "sleep_quality": "poor|average|good",
        "stress_level": "low|moderate|high",
        "barriers": ["if any mentioned"],
        "wins": ["if any mentioned"]
    }},
    "conversation_complete": true,
    "confidence": 0.80
}}"""

    def _build_evening_checkin_system_prompt(self, primary_goal: str = "wellness") -> str:
        """Build system prompt for evening check-ins"""
        
        goal_focus = ""
        if primary_goal == "fitness":
            goal_focus = "- Workout completion\n- Nutrition adherence\n- Recovery prep"
        elif primary_goal == "sleep":
            goal_focus = "- Wind-down routine start\n- Screen time limits\n- Bedroom environment prep"
        elif primary_goal == "stress":
            goal_focus = "- Reflection on daily stressors\n- Gratitude/wins\n- Relaxation state"
        else:
            goal_focus = "- Daily wins\n- Overall balance\n- Prep for tomorrow"

        return f"""You are conducting an evening check-in for a user with PRIMARY GOAL: {primary_goal.upper()}.

Your goal: Help the user reflect on their day and prepare for rest.

Ask about:
{goal_focus}
- One win from today

Keep it brief and calming.

Respond with JSON:
{{
    "agent_response": "Your evening message",
    "extracted_info": {{
        "day_rating": "1-10",
        "completed_tasks": ["list"],
        "mood": "current mood"
    }},
    "conversation_complete": true,
    "confidence": 0.80
}}"""
    
    def _build_daily_checkin_user_prompt(
        self,
        conversation_history: List[Dict],
        user_message: str,
        extracted_data: Dict[str, Any]
    ) -> str:
        """Build user prompt for daily check-in"""
        
        return f"""User's check-in response: "{user_message}"

Extract their current state and respond supportively.

Generate the JSON response."""


# Singleton instance
chat_agent = ChatAgent()
