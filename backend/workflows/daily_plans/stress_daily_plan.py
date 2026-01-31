"""
Stress Daily Plan Generator
For users whose primary goal is stress/anxiety management
"""
from typing import Dict, Any, List
from workflows.daily_plans.base_plan_generator import BaseDailyPlanGenerator


class StressDailyPlanGenerator(BaseDailyPlanGenerator):
    """
    Generates daily plans for stress/anxiety-focused users.
    
    Primary Focus (70%):
    - Stress management techniques
    - Meditation/breathing exercises
    - Emotional support check-ins
    - Cortisol management
    
    Supporting (30%):
    - Light movement (reduces stress)
    - Sleep optimization (stress affects sleep)
    - Nutrition for mood (brain chemistry)
    """
    
    def __init__(self):
        super().__init__(goal_type="stress")
    
    async def generate(
        self,
        user_profile: Dict[str, Any],
        biometrics: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate stress-focused daily plan.
        """
        # Extract key data
        stress_level = biometrics.get("stress_level", "medium")
        energy_level = biometrics.get("energy_level", "medium")
        sleep_quality = biometrics.get("sleep_quality", 3)
        
        # Get stress goal details
        goal_details = user_profile.get("goal_details", {})
        stress_source = goal_details.get("stress_source", "work")  # work, relationships, health, general
        stress_triggers = goal_details.get("triggers", [])
        
        # PRIMARY FOCUS (70%): Stress management
        primary_focus = await self._generate_stress_focus(
            stress_level, stress_source, stress_triggers, context
        )
        
        # SUPPORTING (30%): Movement, sleep, nutrition
        supporting_activities = self._generate_supporting_activities(
            energy_level, sleep_quality, stress_level
        )
        
        # Build morning briefing
        user_name = user_profile.get("display_name", "there")
        morning_briefing = self._build_morning_briefing(
            user_name, primary_focus, supporting_activities, biometrics
        )
        
        # Generate tasks
        tasks = self._generate_tasks(primary_focus, supporting_activities)
        
        return {
            "goal_type": "stress",
            "primary_focus": primary_focus,
            "supporting_activities": supporting_activities,
            "morning_briefing": morning_briefing,
            "tasks": tasks,
            "interventions": context.get("interventions", []),
            "success_metrics": self._calculate_success_metrics({
                "primary_focus": primary_focus,
                "supporting_activities": supporting_activities
            }),
            "focus_split": self._calculate_focus_split(0.7)
        }
    
    async def _generate_stress_focus(
        self,
        stress_level: str,
        stress_source: str,
        stress_triggers: List[str],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate primary stress management activities.
        """
        # Determine intervention intensity based on stress level
        if stress_level in ["very_high", "high"]:
            intervention_frequency = "high"  # Multiple check-ins
            breathing_breaks = 4
            meditation_duration = 20
        elif stress_level == "medium":
            intervention_frequency = "medium"
            breathing_breaks = 3
            meditation_duration = 15
        else:
            intervention_frequency = "low"
            breathing_breaks = 2
            meditation_duration = 10
        
        # Get context-specific stressors
        barriers = context.get("barriers", [])
        schedule = context.get("schedule", [])
        
        return {
            "stress_assessment": {
                "current_level": stress_level,
                "primary_source": stress_source,
                "triggers": stress_triggers,
                "intervention_frequency": intervention_frequency
            },
            "meditation_schedule": {
                "morning_session": {
                    "duration_minutes": meditation_duration,
                    "type": "mindfulness",
                    "timing": "After waking, before checking phone"
                },
                "midday_session": {
                    "duration_minutes": 10,
                    "type": "body_scan",
                    "timing": "Lunch break"
                },
                "evening_session": {
                    "duration_minutes": meditation_duration,
                    "type": "relaxation",
                    "timing": "Before bed"
                }
            },
            "breathing_exercises": {
                "frequency": f"{breathing_breaks}x throughout day",
                "scheduled_times": self._schedule_breathing_breaks(breathing_breaks),
                "techniques": [
                    {"name": "Box Breathing", "pattern": "4-4-4-4", "use": "Acute stress moments"},
                    {"name": "4-7-8 Breathing", "pattern": "Inhale 4, Hold 7, Exhale 8", "use": "Calming before sleep"},
                    {"name": "Physiological Sigh", "pattern": "2 inhales, long exhale", "use": "Quick stress relief"}
                ]
            },
            "emotional_support": {
                "check_ins": [
                    {"time": "morning", "prompt": "How are you feeling today? (1-10)"},
                    {"time": "midday", "prompt": "Stress check: What's your current level?"},
                    {"time": "evening", "prompt": "Reflect: What went well today?"}
                ],
                "journaling": {
                    "frequency": "Daily",
                    "prompts": [
                        "What am I grateful for today?",
                        "What triggered stress today?",
                        "How did I handle it?",
                        "What can I do differently tomorrow?"
                    ]
                }
            },
            "cortisol_management": {
                "avoid": [
                    "Excessive caffeine (increases cortisol)",
                    "Intense exercise when highly stressed",
                    "Skipping meals (blood sugar crashes increase stress)"
                ],
                "include": [
                    "Regular meals (stable blood sugar)",
                    "Omega-3 foods (reduce inflammation)",
                    "Adaptogenic herbs (ashwagandha, rhodiola)"
                ]
            }
        }
    
    def _schedule_breathing_breaks(self, count: int) -> List[str]:
        """Schedule breathing exercise breaks throughout the day."""
        if count == 4:
            return ["10:00 AM", "1:00 PM", "3:00 PM", "6:00 PM"]
        elif count == 3:
            return ["10:00 AM", "2:00 PM", "5:00 PM"]
        else:
            return ["12:00 PM", "4:00 PM"]
    
    def _generate_supporting_activities(
        self,
        energy_level: str,
        sleep_quality: int,
        stress_level: str
    ) -> Dict[str, Any]:
        """
        Generate supporting activities (30% focus).
        Movement, sleep, nutrition that support stress management.
        """
        # Determine movement intensity based on stress
        if stress_level in ["very_high", "high"]:
            movement_type = "gentle"
            movement_recommendation = "Light walk or gentle yoga (high stress + intense exercise = cortisol overload)"
        else:
            movement_type = "moderate"
            movement_recommendation = "Moderate exercise helps manage stress (30-45 min)"
        
        return {
            "movement": {
                "type": movement_type,
                "recommendation": movement_recommendation,
                "options": [
                    "Nature walk (reduces cortisol)",
                    "Gentle yoga (activates parasympathetic)",
                    "Swimming (meditative movement)",
                    "Tai chi (mindful movement)"
                ],
                "avoid": "HIIT or max intensity (elevates cortisol when already stressed)"
            },
            "sleep_optimization": {
                "priority": "high",  # Stress and sleep are deeply connected
                "recommendation": "Poor sleep increases stress sensitivity - prioritize 7-8 hours",
                "actions": [
                    "Consistent bedtime (reduces cortisol)",
                    "Wind-down routine (signals safety to nervous system)",
                    "Magnesium supplement (calms nervous system)"
                ]
            },
            "nutrition": {
                "focus": "Mood-stabilizing foods",
                "recommendations": [
                    "Complex carbs (serotonin production)",
                    "Omega-3 rich foods (salmon, walnuts - reduce inflammation)",
                    "Dark chocolate (small amounts - mood boost)",
                    "Fermented foods (gut-brain axis)"
                ],
                "avoid": [
                    "Excessive caffeine (anxiety trigger)",
                    "Alcohol (disrupts sleep, worsens anxiety)",
                    "High sugar (blood sugar crashes = mood crashes)"
                ],
                "timing": "Regular meals every 3-4 hours (stable blood sugar = stable mood)"
            }
        }
    
    def _get_intervention_priority(self, intervention_type: str) -> int:
        """
        Priority scores for stress-focused users.
        Stress and emotional interventions are highest priority.
        """
        priorities = {
            "stress": 10,  # Highest - this is the primary goal
            "emotional": 9,  # Critical for mental health
            "sleep": 8,  # High - stress ruins sleep, poor sleep worsens stress
            "barrier": 7,  # High - removes stress triggers
            "recovery": 5,  # Supporting
            "nutrition": 6  # Medium - affects mood
        }
        return priorities.get(intervention_type, 4)
    
    def _build_morning_briefing(
        self,
        user_name: str,
        primary_focus: Dict[str, Any],
        supporting_activities: Dict[str, Any],
        biometrics: Dict[str, Any]
    ) -> str:
        """
        Build stress-focused morning briefing.
        """
        stress_level = biometrics.get("stress_level", "medium")
        assessment = primary_focus["stress_assessment"]
        breathing = primary_focus["breathing_exercises"]
        meditation = primary_focus["meditation_schedule"]
        
        briefing = f"Good morning, {user_name}.\n\n"
        
        if stress_level in ["high", "very_high"]:
            briefing += f"⚠️ Stress level is {stress_level}. Today's plan focuses on managing this.\n\n"
        else:
            briefing += f"Stress level: {stress_level}. Let's maintain balance today.\n\n"
        
        briefing += f"Today's focus: {assessment['primary_source']} stress management\n\n"
        briefing += f"Scheduled support:\n"
        briefing += f"- Morning meditation: {meditation['morning_session']['duration_minutes']} min (before checking phone)\n"
        briefing += f"- {breathing['frequency']} breathing exercise breaks ({', '.join(breathing['scheduled_times'])})\n"
        briefing += f"- {supporting_activities['movement']['recommendation']}\n\n"
        
        sleep_quality = biometrics.get("sleep_quality", 3)
        if sleep_quality < 3:
            briefing += f"Note: Sleep was low ({sleep_quality}/5) - this can increase stress sensitivity. Prioritize rest tonight.\n"
        
        return briefing
    
    def _generate_tasks(
        self,
        primary_focus: Dict[str, Any],
        supporting_activities: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Generate actionable tasks for stress-focused day.
        """
        meditation = primary_focus["meditation_schedule"]
        breathing = primary_focus["breathing_exercises"]
        emotional = primary_focus["emotional_support"]
        
        tasks = [
            {
                "time": "morning",
                "category": "meditation",
                "task": f"{meditation['morning_session']['duration_minutes']} min mindfulness meditation",
                "priority": "critical"
            },
            {
                "time": "morning",
                "category": "check_in",
                "task": emotional["check_ins"][0]["prompt"],
                "priority": "high"
            }
        ]
        
        # Add breathing breaks
        for break_time in breathing["scheduled_times"]:
            tasks.append({
                "time": break_time,
                "category": "breathing",
                "task": "3-minute breathing exercise (Box Breathing or Physiological Sigh)",
                "priority": "high"
            })
        
        # Add movement
        tasks.append({
            "time": "midday",
            "category": "movement",
            "task": supporting_activities["movement"]["recommendation"],
            "priority": "medium"
        })
        
        # Add evening tasks
        tasks.extend([
            {
                "time": "evening",
                "category": "meditation",
                "task": f"{meditation['evening_session']['duration_minutes']} min relaxation meditation",
                "priority": "high"
            },
            {
                "time": "evening",
                "category": "journaling",
                "task": "5-minute reflection journal",
                "priority": "medium"
            }
        ])
        
        return tasks


# Singleton instance
stress_daily_plan_generator = StressDailyPlanGenerator()
