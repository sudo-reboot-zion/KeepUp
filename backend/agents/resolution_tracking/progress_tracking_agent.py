"""
Progress Tracking Agent
Analyzes adherence patterns and detects early warning signs
"""
from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from tools.rag_tool import rag_tool
import json
from agents.constraint_framework import INDIVIDUAL_AGENT_PROMPT


class ProgressTrackingAgent(BaseAgent):
    """
    Tracks user progress and detects concerning patterns
    
    Responsibilities:
    - Calculate adherence metrics
    - Identify skip patterns
    - Detect trend changes (improving vs declining)
    - Compare to research on habit formation timelines
    """
    
    def __init__(self):
        super().__init__(
            name="Progress Tracking Agent",
            description="Analyzes workout adherence and detects patterns that predict success or failure",
            model="llama-3.3-70b-versatile"
        )
    
    async def analyze(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze progress and adherence patterns
        
        Input:
            - current_week: int
            - workouts_completed: int
            - workouts_target: int
            - adherence_rate: float
            - skip_pattern: List[bool] (True=completed, False=skipped)
            - user_profile: Dict
            
        Returns:
            - analysis: Dict with metrics and insights
            - trend: str (improving/stable/declining)
            - concerns: List[str]
            - confidence: float
        """
        
        # Extract inputs
        current_week = input_data.get("current_week", 1)
        completed = input_data.get("workouts_completed", 0)
        target = input_data.get("workouts_target", 3)
        adherence = input_data.get("adherence_rate", 0.0)
        skip_pattern = input_data.get("skip_pattern", [])
        user_profile = input_data.get("user_profile", {})
        user_memory = input_data.get("user_memory", {})
        
        # Calculate metrics
        metrics = self._calculate_metrics(skip_pattern, completed, target, adherence)
        
        # Query RAG for habit formation context
        rag_context = await self._get_habit_research(current_week, adherence)
        
        # Build analysis prompt
        system_prompt = self._build_system_prompt(rag_context)
        user_prompt = self._build_user_prompt(
            current_week, completed, target, adherence, skip_pattern, metrics, user_memory
        )
        
        # Call LLM
        response = await self._call_llm(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.3,
            max_tokens=1200
        )
        
        analysis = self._parse_json_response(response)
        
        return {
            "analysis": analysis,
            "metrics": metrics,
            "agent_name": self.name,
            "confidence": analysis.get("confidence", 0.0)
        }
    
    def _calculate_metrics(
        self, 
        skip_pattern: List[bool], 
        completed: int, 
        target: int,
        adherence: float
    ) -> Dict[str, Any]:
        """Calculate detailed adherence metrics"""
        
        metrics = {
            "adherence_rate": adherence,
            "workouts_completed": completed,
            "workouts_target": target,
            "deficit": target - completed
        }
        
        if skip_pattern:
            # Consecutive skips (most recent)
            consecutive_skips = 0
            for did_workout in reversed(skip_pattern):
                if did_workout:
                    break
                consecutive_skips += 1
            
            # Longest skip streak
            max_skip_streak = 0
            current_streak = 0
            for did_workout in skip_pattern:
                if not did_workout:
                    current_streak += 1
                    max_skip_streak = max(max_skip_streak, current_streak)
                else:
                    current_streak = 0
            
            # Consistency score (percentage of planned workout days hit)
            total_days = len(skip_pattern)
            completed_days = sum(1 for d in skip_pattern if d)
            consistency = completed_days / total_days if total_days > 0 else 0.0
            
            metrics.update({
                "consecutive_skips": consecutive_skips,
                "max_skip_streak": max_skip_streak,
                "consistency_score": consistency,
                "total_days_tracked": total_days
            })
        
        return metrics
    
    async def _get_habit_research(self, current_week: int, adherence: float) -> str:
        """Query RAG for relevant habit formation research"""
        
        # Determine what research is most relevant
        if current_week <= 4:
            query = "habit formation first month critical period"
        elif adherence < 0.5:
            query = "recovering from missed workouts adherence"
        else:
            query = "maintaining workout habits long term"
        
        # Query RAG
        result = await rag_tool.search_psychology(query, k=2)
        
        if result.get("success"):
            return result.get("context", "")
        else:
            return "No specific research found."
    
    def _build_system_prompt(self, rag_context: str) -> str:
        """Build system prompt with research context"""
        constraint_prompt = INDIVIDUAL_AGENT_PROMPT.format(
            agent_name="Progress Tracking Agent",
            specialty="tracking fitness adherence and identifying success patterns"
        )
        return constraint_prompt + f"""

You are a progress tracking expert who analyzes workout adherence patterns.

Your role:
- Evaluate adherence metrics objectively
- Identify concerning patterns early
- Provide actionable insights
- Reference habit formation research

Relevant research:
{rag_context}

Key patterns to watch for:
- Week 3-4 cliff (most common quit period)
- Consecutive skips (3+ is concerning)
- Weekend vs weekday patterns
- Declining trend over time
- All-or-nothing behavior

Respond with JSON:
{{
    "overall_assessment": "on_track|concerning|high_risk",
    "trend": "improving|stable|declining",
    "key_metrics": {{
        "adherence_rate": 0.67,
        "consistency_score": 0.75,
        "streak_analysis": "description"
    }},
    "concerns": ["specific concern 1", "concern 2"],
    "positive_indicators": ["what's going well"],
    "recommendations": ["actionable suggestion 1", "suggestion 2"],
    "confidence": 0.85
}}"""
    
    def _build_user_prompt(
        self,
        current_week: int,
        completed: int,
        target: int,
        adherence: float,
        skip_pattern: List[bool],
        metrics: Dict[str, Any],
        user_memory: Dict[str, Any] = None
    ) -> str:
        """Build user prompt with progress data"""
        
        # Format skip pattern for readability
        pattern_str = "".join(["✓" if d else "✗" for d in skip_pattern[-14:]])
        
        # Format memory
        memory_context = ""
        if user_memory:
            failures = user_memory.get("by_type", {}).get("failure_pattern", [])
            if failures:
                memory_context = "\nPAST FAILURE PATTERNS:\n" + "\n".join(
                    [f"- {f['content'].get('pattern', '')}" for f in failures[:3]]
                )
        
        return f"""Analyze this user's progress:

CURRENT STATUS:
- Week: {current_week}
- This Week: {completed}/{target} workouts completed
- Adherence Rate: {adherence:.1%}

RECENT PATTERN (last 14 days):
{pattern_str}
(✓ = completed, ✗ = skipped)

CALCULATED METRICS:
{json.dumps(metrics, indent=2)}
{memory_context}

Your task:
1. Assess overall progress trajectory
2. Identify any concerning patterns (especially if matching past failures)
3. Provide specific, actionable recommendations
4. Note what's going well (positive reinforcement)

Generate the JSON response now."""


# Singleton instance
progress_tracking_agent = ProgressTrackingAgent()
