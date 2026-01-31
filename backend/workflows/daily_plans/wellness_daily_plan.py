"""
Wellness Daily Plan Generator
For users whose primary goal is general wellness/energy/balance
"""
from typing import Dict, Any, List
from workflows.daily_plans.base_plan_generator import BaseDailyPlanGenerator


class WellnessDailyPlanGenerator(BaseDailyPlanGenerator):
    """
    Generates daily plans for wellness-focused users.
    
    Balanced Focus:
    - Moderate exercise (energy without depletion)
    - Nutrition for sustained energy
    - Sleep optimization
    - Stress prevention
    - Holistic health monitoring
    
    Unlike other goals, wellness users get balanced attention across all dimensions.
    """
    
    def __init__(self):
        super().__init__(goal_type="wellness")
    
    async def generate(
        self,
        user_profile: Dict[str, Any],
        biometrics: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate balanced wellness plan.
        """
        # Extract key data
        sleep_quality = biometrics.get("sleep_quality", 3)
        energy_level = biometrics.get("energy_level", "medium")
        stress_level = biometrics.get("stress_level", "low")
        readiness_score = biometrics.get("readiness_score", 0.7)
        
        # BALANCED FOCUS: All dimensions get attention
        primary_focus = await self._generate_wellness_focus(
            user_profile, biometrics, readiness_score
        )
        
        # Build morning briefing
        user_name = user_profile.get("display_name", "there")
        morning_briefing = self._build_morning_briefing(
            user_name, primary_focus, {}, biometrics
        )
        
        # Generate tasks
        tasks = self._generate_tasks(primary_focus, {})
        
        return {
            "goal_type": "wellness",
            "primary_focus": primary_focus,
            "supporting_activities": {},  # Everything is primary for wellness
            "morning_briefing": morning_briefing,
            "tasks": tasks,
            "interventions": context.get("interventions", []),
            "success_metrics": self._calculate_success_metrics({
                "primary_focus": primary_focus
            }),
            "focus_split": {"balanced": 1.0}  # No 70/30 split - everything is balanced
        }
    
    async def _generate_wellness_focus(
        self,
        user_profile: Dict[str, Any],
        biometrics: Dict[str, Any],
        readiness_score: float
    ) -> Dict[str, Any]:
        """
        Generate balanced wellness activities.
        All dimensions get equal attention.
        """
        return {
            "movement": {
                "type": "moderate",
                "recommendation": "30-45 min moderate exercise (builds energy without depletion)",
                "options": [
                    "Brisk walk",
                    "Light jog",
                    "Yoga flow",
                    "Swimming",
                    "Cycling"
                ],
                "intensity": "60-70% max heart rate",
                "purpose": "Energy, mood, cardiovascular health"
            },
            "nutrition": {
                "focus": "Sustained energy and overall health",
                "principles": [
                    "Balanced macros (40% carbs, 30% protein, 30% fat)",
                    "Whole foods > processed",
                    "Colorful vegetables (phytonutrients)",
                    "Adequate hydration (2-3L water)"
                ],
                "meal_timing": "Regular meals every 3-4 hours",
                "supplements": ["Multivitamin", "Omega-3", "Vitamin D"]
            },
            "sleep": {
                "target_hours": 7.5,
                "quality_focus": "Consistent schedule",
                "recommendations": [
                    "Same bedtime/wake time (±30 min)",
                    "Wind-down routine",
                    "Cool, dark bedroom"
                ]
            },
            "stress_management": {
                "approach": "Prevention over intervention",
                "daily_practices": [
                    "10-minute morning meditation",
                    "Breathing breaks when needed",
                    "Evening reflection/gratitude"
                ],
                "purpose": "Maintain low baseline stress"
            },
            "energy_optimization": {
                "morning_routine": [
                    "Sunlight exposure (15 min)",
                    "Movement (walk or stretch)",
                    "Hydration (16 oz water)",
                    "Protein-rich breakfast"
                ],
                "throughout_day": [
                    "Regular movement breaks",
                    "Avoid energy crashes (stable blood sugar)",
                    "Social connection (energy boost)"
                ]
            },
            "holistic_health": {
                "weekly_goals": [
                    "3-4 moderate workouts",
                    "7-8 hours sleep nightly",
                    "Stress level: low-medium",
                    "Balanced nutrition",
                    "Social connection",
                    "Time in nature"
                ],
                "philosophy": "Sustainable health > extreme optimization"
            }
        }
    
    def _get_intervention_priority(self, intervention_type: str) -> int:
        """
        Priority scores for wellness-focused users.
        All interventions get relatively equal weight.
        """
        priorities = {
            "sleep": 7,
            "stress": 7,
            "recovery": 7,
            "nutrition": 7,
            "barrier": 8,  # Slightly higher - removes obstacles
            "energy": 7
        }
        return priorities.get(intervention_type, 6)
    
    def _build_morning_briefing(
        self,
        user_name: str,
        primary_focus: Dict[str, Any],
        supporting_activities: Dict[str, Any],
        biometrics: Dict[str, Any]
    ) -> str:
        """
        Build wellness-focused morning briefing.
        """
        energy_level = biometrics.get("energy_level", "medium")
        sleep_quality = biometrics.get("sleep_quality", 3)
        
        briefing = f"Good morning, {user_name}!\n\n"
        briefing += f"Energy level: {energy_level} | Sleep quality: {sleep_quality}/5\n\n"
        briefing += "Today's balanced wellness plan:\n"
        briefing += f"- {primary_focus['movement']['recommendation']}\n"
        briefing += f"- {primary_focus['nutrition']['focus']}\n"
        briefing += f"- {primary_focus['stress_management']['daily_practices'][0]}\n"
        briefing += f"- Sleep target: {primary_focus['sleep']['target_hours']} hours\n\n"
        briefing += "Focus: Sustainable health across all dimensions 🌟"
        
        return briefing
    
    def _generate_tasks(
        self,
        primary_focus: Dict[str, Any],
        supporting_activities: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Generate balanced tasks for wellness day.
        """
        return [
            {
                "time": "morning",
                "category": "energy",
                "task": "Morning routine: Sunlight + movement + hydration",
                "priority": "high"
            },
            {
                "time": "morning",
                "category": "mindfulness",
                "task": "10-minute meditation",
                "priority": "medium"
            },
            {
                "time": "midday",
                "category": "movement",
                "task": primary_focus["movement"]["recommendation"],
                "priority": "high"
            },
            {
                "time": "throughout_day",
                "category": "nutrition",
                "task": "Balanced meals every 3-4 hours",
                "priority": "medium"
            },
            {
                "time": "throughout_day",
                "category": "hydration",
                "task": "Water intake: 2-3L target",
                "priority": "medium"
            },
            {
                "time": "evening",
                "category": "reflection",
                "task": "5-minute gratitude/reflection",
                "priority": "low"
            },
            {
                "time": "evening",
                "category": "sleep",
                "task": f"Bedtime routine for {primary_focus['sleep']['target_hours']}h sleep",
                "priority": "medium"
            }
        ]


# Singleton instance
wellness_daily_plan_generator = WellnessDailyPlanGenerator()
