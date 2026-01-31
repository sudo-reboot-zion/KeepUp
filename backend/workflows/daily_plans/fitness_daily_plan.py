"""
Fitness Daily Plan Generator
For users whose primary goal is fitness (weight loss, strength, endurance, sport-specific)
"""
from typing import Dict, Any, List
from workflows.daily_plans.base_plan_generator import BaseDailyPlanGenerator


class FitnessDailyPlanGenerator(BaseDailyPlanGenerator):
    """
    Generates daily plans for fitness-focused users.
    
    Primary Focus (70%):
    - Workout plan for the day
    - Nutrition targets and meal suggestions
    - Progress tracking
    
    Supporting (30%):
    - Sleep quality monitoring (affects recovery)
    - Stress level check (affects performance)
    - Energy optimization
    """
    
    def __init__(self):
        super().__init__(goal_type="fitness")
    
    async def generate(
        self,
        user_profile: Dict[str, Any],
        biometrics: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate fitness-focused daily plan.
        """
        # Extract key data
        readiness_score = biometrics.get("readiness_score", 0.7)
        sleep_quality = biometrics.get("sleep_quality", 3)
        energy_level = biometrics.get("energy_level", "medium")
        stress_level = biometrics.get("stress_level", "low")
        soreness = biometrics.get("soreness_level", "low")
        
        interventions = context.get("interventions", [])
        barriers = context.get("barriers", [])
        
        # PRIMARY FOCUS (70%): Fitness activities
        primary_focus = await self._generate_fitness_focus(
            user_profile, biometrics, readiness_score
        )
        
        # SUPPORTING (30%): Sleep, stress, recovery
        supporting_activities = self._generate_supporting_activities(
            sleep_quality, stress_level, energy_level
        )
        
        # Prioritize interventions
        prioritized_interventions = self._prioritize_interventions(interventions)
        
        # Build morning briefing
        user_name = user_profile.get("display_name", "there")
        morning_briefing = self._build_morning_briefing(
            user_name, primary_focus, supporting_activities, biometrics
        )
        
        # Generate tasks
        tasks = self._generate_tasks(primary_focus, supporting_activities)
        
        return {
            "goal_type": "fitness",
            "primary_focus": primary_focus,
            "supporting_activities": supporting_activities,
            "morning_briefing": morning_briefing,
            "tasks": tasks,
            "interventions": prioritized_interventions,
            "success_metrics": self._calculate_success_metrics({
                "primary_focus": primary_focus,
                "supporting_activities": supporting_activities
            }),
            "focus_split": self._calculate_focus_split(0.7)
        }
    
    async def _generate_fitness_focus(
        self,
        user_profile: Dict[str, Any],
        biometrics: Dict[str, Any],
        readiness_score: float
    ) -> Dict[str, Any]:
        """
        Generate the primary fitness activities for the day.
        """
        # Get user's fitness goal details
        goal_details = user_profile.get("goal_details", {})
        fitness_type = goal_details.get("fitness_type", "general")  # weight_loss, strength, endurance
        
        # Adjust intensity based on readiness
        if readiness_score >= 0.8:
            intensity = "high"
            workout_duration = 60
        elif readiness_score >= 0.6:
            intensity = "moderate"
            workout_duration = 45
        else:
            intensity = "light"
            workout_duration = 30
        
        # Get nutrition targets
        nutrition = self._calculate_nutrition_targets(user_profile, fitness_type)
        
        return {
            "workout": {
                "type": fitness_type,
                "intensity": intensity,
                "duration_minutes": workout_duration,
                "scheduled_time": self._get_optimal_workout_time(user_profile),
                "exercises": []  # Would be populated by workout generation agent
            },
            "nutrition": nutrition,
            "progress_tracking": {
                "metrics_to_log": ["weight", "body_measurements", "workout_performance"],
                "photo_check": self._should_take_progress_photo(user_profile)
            }
        }
    
    def _calculate_nutrition_targets(
        self,
        user_profile: Dict[str, Any],
        fitness_type: str
    ) -> Dict[str, Any]:
        """
        Calculate nutrition targets based on fitness goal.
        """
        # Simplified - would use more sophisticated calculation
        if fitness_type == "weight_loss":
            return {
                "calories": 1800,
                "protein_grams": 140,
                "carbs_grams": 150,
                "fat_grams": 60,
                "meal_timing": "3 main meals + 1 snack"
            }
        elif fitness_type == "strength":
            return {
                "calories": 2400,
                "protein_grams": 180,
                "carbs_grams": 250,
                "fat_grams": 80,
                "meal_timing": "4-5 meals, protein every 3-4 hours"
            }
        else:  # general fitness
            return {
                "calories": 2000,
                "protein_grams": 150,
                "carbs_grams": 200,
                "fat_grams": 70,
                "meal_timing": "3 balanced meals"
            }
    
    def _get_optimal_workout_time(self, user_profile: Dict[str, Any]) -> str:
        """
        Determine optimal workout time based on user's schedule and preferences.
        """
        # Would integrate with calendar agent
        return "6:00 PM"  # Placeholder
    
    def _should_take_progress_photo(self, user_profile: Dict[str, Any]) -> bool:
        """
        Determine if today is a progress photo day.
        """
        # Every 2 weeks
        return False  # Placeholder
    
    def _generate_supporting_activities(
        self,
        sleep_quality: int,
        stress_level: str,
        energy_level: str
    ) -> Dict[str, Any]:
        """
        Generate supporting activities (30% focus).
        These support fitness but aren't the primary focus.
        """
        activities = {
            "sleep_optimization": {},
            "stress_management": {},
            "recovery": {}
        }
        
        # Sleep monitoring (affects recovery)
        if sleep_quality < 3:
            activities["sleep_optimization"] = {
                "priority": "high",
                "recommendation": "Poor sleep is affecting recovery. Target 8 hours tonight.",
                "actions": [
                    "Set bedtime alarm for 10:00 PM",
                    "Avoid caffeine after 2 PM",
                    "Wind-down routine at 9:30 PM"
                ]
            }
        else:
            activities["sleep_optimization"] = {
                "priority": "low",
                "recommendation": f"Sleep quality is good ({sleep_quality}/5). Maintain current routine.",
                "actions": ["Continue current sleep schedule"]
            }
        
        # Stress check (affects performance)
        if stress_level in ["high", "very_high"]:
            activities["stress_management"] = {
                "priority": "medium",
                "recommendation": "High stress can impair workout performance. Consider lighter session.",
                "actions": [
                    "10-minute meditation before workout",
                    "Reduce workout intensity 20%",
                    "Focus on form over weight"
                ]
            }
        
        # Recovery activities
        activities["recovery"] = {
            "stretching": "10 minutes post-workout",
            "hydration": "3L water target",
            "active_recovery": "20-minute walk if feeling good"
        }
        
        return activities
    
    def _get_intervention_priority(self, intervention_type: str) -> int:
        """
        Priority scores for fitness-focused users.
        Higher = more important
        """
        priorities = {
            "recovery": 10,  # Highest - prevents injury
            "nutrition": 9,  # Critical for fitness goals
            "sleep": 7,  # Important but supporting
            "stress": 6,  # Supporting
            "barrier": 8  # High - removes obstacles
        }
        return priorities.get(intervention_type, 5)
    
    def _build_morning_briefing(
        self,
        user_name: str,
        primary_focus: Dict[str, Any],
        supporting_activities: Dict[str, Any],
        biometrics: Dict[str, Any]
    ) -> str:
        """
        Build fitness-focused morning briefing.
        """
        workout = primary_focus["workout"]
        nutrition = primary_focus["nutrition"]
        
        briefing = f"Good morning, {user_name}!\n\n"
        briefing += f"Today's focus: {workout['type'].replace('_', ' ').title()} ({workout['intensity']} intensity)\n"
        briefing += f"Workout: {workout['duration_minutes']} min at {workout['scheduled_time']}\n"
        briefing += f"Nutrition: {nutrition['calories']} cal target, {nutrition['protein_grams']}g protein\n\n"
        
        # Add sleep context if relevant
        sleep_quality = biometrics.get("sleep_quality", 3)
        if sleep_quality < 3:
            briefing += f"⚠️ Sleep was low ({sleep_quality}/5) - workout adjusted to {workout['intensity']} intensity\n"
        
        briefing += f"\nSleep target tonight: 10:30 PM for optimal recovery"
        
        return briefing
    
    def _generate_tasks(
        self,
        primary_focus: Dict[str, Any],
        supporting_activities: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Generate actionable tasks for fitness-focused day.
        """
        workout = primary_focus["workout"]
        nutrition = primary_focus["nutrition"]
        
        tasks = [
            {
                "time": "morning",
                "category": "nutrition",
                "task": f"Breakfast: Protein-rich meal ({nutrition['protein_grams']/3:.0f}g protein target)",
                "priority": "high"
            },
            {
                "time": workout["scheduled_time"],
                "category": "workout",
                "task": f"{workout['type'].replace('_', ' ').title()} workout - {workout['duration_minutes']} min",
                "priority": "critical"
            },
            {
                "time": "throughout_day",
                "category": "nutrition",
                "task": f"Track meals - {nutrition['calories']} cal budget remaining",
                "priority": "high"
            },
            {
                "time": "evening",
                "category": "recovery",
                "task": "Post-workout: Stretching + protein shake",
                "priority": "medium"
            }
        ]
        
        # Add sleep task if sleep optimization is high priority
        if supporting_activities["sleep_optimization"].get("priority") == "high":
            tasks.append({
                "time": "9:30 PM",
                "category": "sleep",
                "task": "Wind-down routine (affects tomorrow's recovery)",
                "priority": "high"
            })
        
        return tasks


# Singleton instance
fitness_daily_plan_generator = FitnessDailyPlanGenerator()
