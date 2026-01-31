"""
Base Agent Class - All  agents inherit from this
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime
import json
from langchain_groq import ChatGroq
from core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession




class BaseAgent(ABC):
    """Abstract base class for all agents"""

    def __init__(
        self,
        name: str,
        description: str,
        model: str = "llama-3.3-70b-versatile",
        tools: Optional[List[Any]] = None,
        requires_user_context: bool = True
    ):
        self.name = name
        self.description = description
        self.model = model
        self.tools = tools
        self.requires_user_context = requires_user_context
        
        # Opik removed
        callbacks = []

        self.llm = ChatGroq(
            model=model,
            api_key=settings.GROQ_API_KEY,
            temperature=0.3,
            callbacks=callbacks
        )


    async def _get_user_profile(self, user_id: int, db: AsyncSession) -> Dict[str, Any]:
        """
        Fetch user profile from database
        """
        from services.user_service import UserService
        return await UserService.get_user_profile(user_id, db)


    def _build_user_context_prompt(self, user_profile: Dict[str, Any]) -> str:
        """
        Build context about te user for the agent to consider.
        Only called if requires_user_context=True
        """
        context_parts = []

        if age := user_profile.get("age"):
            context_parts.append(f"Age: {age}")
        
        if gender := user_profile.get("gender"):
            context_parts.append(f"Gender: {gender}")

        if gender == "female":
            if cycle_day := user_profile.get("cycle_day"):
                phase = self._get_cycle_phase(cycle_day)
                context_parts.append(f"Menstraul cycle: Day {cycle_day} ({phase})")
                context_parts.append(self._get_phase_considerations(phase))

        if age:
            if age > 50:
                context_parts.append("Consider: Recovery takes longer, joint health")
            elif age < 25:
                context_parts.append("Consider: Hormonal changes, growth spurt")
    
        return "\n".join(context_parts) if context_parts else "No specific user context."

    def _get_cycle_phase(self, day: int) -> str:
        """Determine menstrual cycle phase"""
        if 1 <= day <= 5:
            return "Menstruation"
        elif 6 <= day <= 14:
            return "Follicular - High Energy Phase"
        elif 15 <= day <= 17:
            return "Ovulation"
        elif 18 <= day <= 28:
            return "Luteal - Energy Declining"
        return "Unknown"
    
    def _get_phase_considerations(self, phase: str) -> str:
        """Get training considerations for cycle phase"""
        considerations = {
            "Menstruation": "Lower energy, cramping possible. Lighter workouts, more rest.",
            "Follicular - High Energy Phase": "Peak performance window. Push intensity, try PRs.",
            "Ovulation": "High energy continues. Great time for challenging workouts.",
            "Lutual - Energy Declining": "Progesterone rising, energy drops. Focus on maintenance, expect less."
        }
        return considerations.get(phase, "")


    @abstractmethod

    async def analyze(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Each agent must implement this method 
        Takes input data, returns analysis
        """
        pass

    async def _call_llm(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 1000
    ) -> str:
        """
        Call Groq via Langchain - All agents use this method
        """
        try:
            from langchain_core.messages import SystemMessage, HumanMessage
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]

            response = await self.llm.ainvoke(
                messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.content

        except Exception as e:
            print(f"[{self.name}] LLM call failed: {str(e)}")
            raise

    
    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """
        Safely extract JSON from LLM response (handles ```json blocks)
        """

        try:
        # Try normal JSON first
            return json.loads(response)
        except Exception:
            pass

        try:
            # Remove ```json and ``` markers
            cleaned = response.replace("```json", "").replace("```", "").strip()

            # Find first JSON object
            start = cleaned.find("{")
            end = cleaned.rfind("}") + 1

            if start == -1 or end == -1:
                raise ValueError("No JSON found")

            json_str = cleaned[start:end]
            return json.loads(json_str)

        except Exception as e:
            print(f"[{self.name}] JSON parse error: {e}")
            print(f"RAW RESPONSE:\n{response}")
            return {
            "error": "Failed to parse LLM response",
            "raw_response": response
            }




    async def challenge(
        self,
        proposed_plan: Dict[str, Any],
        challenger_context: Dict[str, Any]
        ) -> Dict[str, Any]:

        """
        Challenge another agent's proposal.
        Returns: support/challenge/conditional
        """
        system_prompt = f"""
                         You are {self.name}.
                         Another agent proposed a plan. Review it through YOUR domain expertise.
                         Your role: {self.description}

                         Respond with JSON:
                         {{
                            "stance": "support|Challenge|conditional",
                            "reasoning": "why you agree/disagree",
                            "concerns": ["specific issues from your domain"],
                            "counter_proposal": "if challenging, what would you suggest instead",
                            "confidence": 0.8
                         }}
                         """

        user_prompt = f"""
                       Proposed Plan: {json.dumps(proposed_plan, indent=2)}
                       Context: {json.dumps(challenger_context, indent=2)}
                       Evaluate this plan from your domain expertise.
                      """

        response = await self._call_llm(system_prompt, user_prompt)
        parsed =  self._parse_json_response(response)

        return {
                "stance": parsed.get("stance", "unknown").lower(),
                "reasoning": parsed.get("reasoning", ""),
                "concerns": parsed.get("concerns", []),
                "counter_proposal": parsed.get("counter_proposal"),
                "confidence": parsed.get("confidence", 0.5),
                "raw": parsed
        }


