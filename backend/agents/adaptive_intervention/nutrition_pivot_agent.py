"""
Nutrition Pivot Agent
Adapts nutrition recommendations based on workout performance and goals
"""
from typing import Dict, Any
from agents.base_agent import BaseAgent
from tools.rag_tool import rag_tool
from tools.tavily_search_tool import tavily_tool
from agents.constraint_framework import INDIVIDUAL_AGENT_PROMPT


class NutritionPivotAgent(BaseAgent):
    """
    Adjusts nutrition strategy when workouts aren't progressing or goals change
    
    Responsibilities:
    - Identify nutrition-related performance issues
    - Recommend macro adjustments
    - Suggest meal timing changes
    - Address energy/recovery problems through diet
    """
    
    def __init__(self):
        super().__init__(
            name="Nutrition Pivot Agent",
            description="Nutritional biochemistry expert who adjusts diet strategy based on performance",
            model="llama-3.3-70b-versatile"
        )
    
    async def analyze(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze nutrition needs and recommend pivots
        
        Input:
            - current_nutrition: Dict (current eating pattern)
            - workout_performance: Dict (energy levels, recovery, strength gains)
            - goals: str (lose_fat, gain_muscle, performance, health)
            - user_profile: Dict
            - context: Dict (sleep, stress, etc.)
            
        Returns:
            - needs_pivot: bool
            - recommended_changes: List[Dict]
            - reasoning: str
            - confidence: float
        """
        
        # Extract inputs
        current_nutrition = input_data.get("current_nutrition", {})
        performance = input_data.get("workout_performance", {})
        goals = input_data.get("goals", "health")
        user_profile = input_data.get("user_profile", {})
        context = input_data.get("context", {})
        
        # Identify nutrition issues
        issues = self._identify_nutrition_issues(performance, context)
        
        # Query RAG for nutrition knowledge
        knowledge = await self._get_nutrition_knowledge(issues, goals)
        
        # Query Tavily for latest nutrition science if needed
        if issues and len(issues) > 2:
            latest_research = await tavily_tool.search_nutrition_info(
                f"nutrition for {goals} and {', '.join(issues[:2])}"
            )
            if latest_research.get("success"):
                knowledge += f"\n\nLATEST RESEARCH:\n{latest_research.get('answer', '')}"
        
        # Build prompt
        system_prompt = self._build_system_prompt(knowledge)
        user_prompt = self._build_user_prompt(
            current_nutrition, performance, goals, issues, user_profile, context
        )
        
        # Call LLM
        response = await self._call_llm(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.3,
            max_tokens=1500
        )
        
        result = self._parse_json_response(response)
        
        return {
            "needs_pivot": result.get("needs_pivot", False),
            "recommended_changes": result.get("recommended_changes", []),
            "reasoning": result.get("reasoning", ""),
            "macro_adjustments": result.get("macro_adjustments", {}),
            "meal_timing_changes": result.get("meal_timing_changes", []),
            "confidence": result.get("confidence", 0.0),
            "agent_name": self.name
        }
    
    def _identify_nutrition_issues(
        self,
        performance: Dict[str, Any],
        context: Dict[str, Any]
    ) -> list:
        """Identify potential nutrition-related issues"""
        issues = []
        
        # Energy issues
        if performance.get("energy_levels") == "low":
            issues.append("chronic_low_energy")
        
        # Recovery issues
        if performance.get("recovery_quality") == "poor":
            issues.append("slow_recovery")
        
        # Strength plateau
        if performance.get("strength_trend") == "plateau":
            issues.append("strength_plateau")
        
        # Sleep issues (nutrition-related)
        if context.get("sleep_quality") == "poor":
            issues.append("sleep_nutrition_link")
        
        # Weight not changing despite effort
        if performance.get("body_composition_change") == "none":
            issues.append("body_comp_stall")
        
        return issues
    
    async def _get_nutrition_knowledge(self, issues: list, goals: str) -> str:
        """Query RAG for relevant nutrition knowledge"""
        knowledge_parts = []
        
        # Query for specific issues
        if "low_energy" in str(issues):
            result = await rag_tool.search_nutrition("energy nutrition pre-workout fueling", k=2)
            if result.get("success"):
                knowledge_parts.append(result.get("context", ""))
        
        if "recovery" in str(issues):
            result = await rag_tool.search_nutrition("post-workout recovery nutrition protein timing", k=2)
            if result.get("success"):
                knowledge_parts.append(result.get("context", ""))
        
        if "plateau" in str(issues):
            result = await rag_tool.search_nutrition("muscle gain protein requirements progressive overload", k=2)
            if result.get("success"):
                knowledge_parts.append(result.get("context", ""))
        
        # Query for goal-specific nutrition
        goal_query_map = {
            "lose_fat": "fat loss nutrition calorie deficit protein preservation",
            "gain_muscle": "muscle gain bulking protein timing anabolic window",
            "performance": "athletic performance carbohydrate timing endurance",
            "health": "general health balanced nutrition micronutrients"
        }
        
        goal_query = goal_query_map.get(goals, "balanced nutrition")
        result = await rag_tool.search_nutrition(goal_query, k=2)
        if result.get("success"):
            knowledge_parts.append(result.get("context", ""))
        
        return "\n\n---\n\n".join(knowledge_parts) if knowledge_parts else "No specific guidelines found."
    
        # Calculate precise macros using Calculator Tool
        from tools.calculator_tool import calculator_tool
        
        # Example calculation logic (simplified for prompt)
        # In a real scenario, the agent would determine these percentages dynamically
        macros = calculator_tool.calculate_macros(
            calories=2500,  # Placeholder - would come from TDEE calc
            protein_pct=0.3,
            fat_pct=0.25,
            carb_pct=0.45
        )
        
        return constraint_prompt + f"""\n\nYou are a nutritional biochemistry expert specializing in performance nutrition.

Your role:
- Identify when nutrition is limiting performance
- Recommend evidence-based dietary adjustments
- Prioritize sustainable, practical changes
- Account for individual context and preferences

Scientific knowledge:
{knowledge}

Key principles:
- Protein: 0.8-1g per lb bodyweight for muscle maintenance/gain
- Carbs: Fuel for performance, adjust based on activity level
- Fats: Essential for hormones, 20-35% of calories
- Timing matters: Pre/post workout nutrition affects performance and recovery
- Sleep nutrition: Avoid heavy meals 3h before bed, consider magnesium

Respond with JSON:
{{
    "needs_pivot": true,
    "recommended_changes": [
        {{
            "change": "Increase protein to {macros['protein_g']}g/day",
            "reason": "Current intake insufficient for recovery",
            "priority": "high",
            "implementation": "Add protein shake post-workout"
        }}
    ],
    "macro_adjustments": {{
        "protein_g": {macros['protein_g']},
        "carbs_g": {macros['carbs_g']},
        "fats_g": {macros['fats_g']},
        "rationale": "Adjusted for hypertrophy and recovery"
    }},
    "meal_timing_changes": [
        "Eat 30-60min before workout",
        "Protein within 2h post-workout"
    ],
    "reasoning": "Detailed explanation of recommendations",
    "confidence": 0.85
}}"""
    
    def _build_user_prompt(
        self,
        current_nutrition: Dict[str, Any],
        performance: Dict[str, Any],
        goals: str,
        issues: list,
        user_profile: Dict[str, Any],
        context: Dict[str, Any]
    ) -> str:
        """Build user prompt with nutrition data"""
        
        issues_text = ", ".join(issues) if issues else "None identified"
        
        return f"""Analyze nutrition and recommend pivots:

CURRENT NUTRITION:
- Protein: {current_nutrition.get('protein_g', 'unknown')}g/day
- Carbs: {current_nutrition.get('carbs_g', 'unknown')}g/day
- Fats: {current_nutrition.get('fats_g', 'unknown')}g/day
- Meal Timing: {current_nutrition.get('meal_timing', 'irregular')}

WORKOUT PERFORMANCE:
- Energy Levels: {performance.get('energy_levels', 'unknown')}
- Recovery Quality: {performance.get('recovery_quality', 'unknown')}
- Strength Trend: {performance.get('strength_trend', 'unknown')}
- Body Composition: {performance.get('body_composition_change', 'unknown')}

GOALS: {goals}

IDENTIFIED ISSUES: {issues_text}

USER PROFILE:
- Weight: {user_profile.get('weight', 'unknown')} kg
- Activity Level: {user_profile.get('activity_level', 'moderate')}
- Dietary Restrictions: {user_profile.get('dietary_restrictions', 'none')}

CONTEXT:
- Sleep: {context.get('sleep_quality', 'unknown')}
- Stress: {context.get('stress_level', 'unknown')}

Your task:
1. Determine if nutrition pivot is needed
2. Recommend specific, actionable changes
3. Prioritize most impactful adjustments
4. Ensure recommendations align with goals

Generate JSON response."""

# Singleton instance
nutrition_pivot_agent = NutritionPivotAgent()
