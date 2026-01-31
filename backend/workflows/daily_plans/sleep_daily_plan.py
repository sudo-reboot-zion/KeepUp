"""
Sleep Daily Plan Generator
For users whose primary goal is sleep improvement
"""
from typing import Dict, Any, List
from workflows.daily_plans.base_plan_generator import BaseDailyPlanGenerator


class SleepDailyPlanGenerator(BaseDailyPlanGenerator):
    """
    Generates daily plans for sleep-focused users.
    
    Primary Focus (70%):
    - Sleep protocol for tonight
    - Circadian rhythm optimization
    - Wind-down routine
    - Sleep environment optimization
    
    Supporting (30%):
    - Light movement (improves sleep quality)
    - Nutrition timing (no late caffeine/heavy meals)
    - Stress management (affects sleep)
    """
    
    def __init__(self):
        super().__init__(goal_type="sleep")
    
    async def generate(
        self,
        user_profile: Dict[str, Any],
        biometrics: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate sleep-focused daily plan.
        """
        # Extract key data
        sleep_quality = biometrics.get("sleep_quality", 3)
        sleep_hours = biometrics.get("sleep_hours", 6.5)
        energy_level = biometrics.get("energy_level", "medium")
        stress_level = biometrics.get("stress_level", "low")
        
        # Get sleep goal details
        goal_details = user_profile.get("goal_details", {})
        target_sleep_hours = goal_details.get("target_sleep_hours", 7.5)
        sleep_issue = goal_details.get("sleep_issue", "quality")  # falling_asleep, staying_asleep, quality
        
        # PRIMARY FOCUS (70%): Sleep optimization
        primary_focus = await self._generate_sleep_focus(
            sleep_quality, sleep_hours, target_sleep_hours, sleep_issue
        )
        
        # SUPPORTING (30%): Movement, nutrition, stress
        supporting_activities = self._generate_supporting_activities(
            energy_level, stress_level, sleep_quality
        )
        
        # Build morning briefing
        user_name = user_profile.get("display_name", "there")
        morning_briefing = self._build_morning_briefing(
            user_name, primary_focus, supporting_activities, biometrics
        )
        
        # Generate tasks
        tasks = self._generate_tasks(primary_focus, supporting_activities)
        
        return {
            "goal_type": "sleep",
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
    
    async def _generate_sleep_focus(
        self,
        sleep_quality: int,
        sleep_hours: float,
        target_hours: float,
        sleep_issue: str
    ) -> Dict[str, Any]:
        """
        Generate primary sleep optimization activities.
        """
        # Calculate sleep debt
        sleep_debt = max(0, target_hours - sleep_hours)
        
        # Determine tonight's protocol based on issue
        if sleep_issue == "falling_asleep":
            protocol = self._get_falling_asleep_protocol()
        elif sleep_issue == "staying_asleep":
            protocol = self._get_staying_asleep_protocol()
        else:  # quality
            protocol = self._get_quality_improvement_protocol()
        
        # Calculate optimal bedtime
        wake_time = "7:00 AM"  # Would get from user preferences
        bedtime = self._calculate_bedtime(wake_time, target_hours)
        
        return {
            "tonight_protocol": protocol,
            "sleep_schedule": {
                "target_bedtime": bedtime,
                "target_wake_time": wake_time,
                "target_hours": target_hours,
                "wind_down_start": self._calculate_wind_down_time(bedtime)
            },
            "circadian_optimization": {
                "morning_sunlight": {
                    "duration_minutes": 15,
                    "timing": "Within 30 min of waking",
                    "purpose": "Anchors circadian rhythm"
                },
                "light_exposure": {
                    "dim_lights_after": "8:00 PM",
                    "blue_light_cutoff": "9:00 PM",
                    "bedroom_darkness": "Complete darkness (blackout curtains)"
                }
            },
            "sleep_environment": {
                "temperature": "65-68°F (18-20°C)",
                "noise": "White noise or silence",
                "bedding": "Clean sheets, comfortable pillows"
            },
            "sleep_debt": sleep_debt,
            "quality_assessment": {
                "last_night": sleep_quality,
                "trend": "improving" if sleep_quality >= 3 else "needs_attention"
            }
        }
    
    def _get_falling_asleep_protocol(self) -> Dict[str, Any]:
        """Protocol for users who struggle to fall asleep."""
        return {
            "type": "falling_asleep",
            "steps": [
                {"time": "2 hours before bed", "action": "No caffeine or stimulants"},
                {"time": "1 hour before bed", "action": "No screens (blue light)"},
                {"time": "30 min before bed", "action": "Wind-down routine (reading, stretching, meditation)"},
                {"time": "Bedtime", "action": "4-7-8 breathing technique (3 cycles)"},
                {"time": "If not asleep in 20 min", "action": "Get up, do calming activity, return when sleepy"}
            ],
            "supplements": ["Magnesium glycinate 400mg", "L-theanine 200mg (optional)"],
            "avoid": ["Alcohol", "Heavy meals", "Intense exercise after 6 PM"]
        }
    
    def _get_staying_asleep_protocol(self) -> Dict[str, Any]:
        """Protocol for users who wake during the night."""
        return {
            "type": "staying_asleep",
            "steps": [
                {"time": "Evening", "action": "Limit fluids 2 hours before bed"},
                {"time": "Dinner", "action": "Avoid spicy/acidic foods"},
                {"time": "Bedtime", "action": "Ensure room is cool (65-68°F)"},
                {"time": "If wake up", "action": "Don't check time, practice body scan meditation"}
            ],
            "supplements": ["Magnesium glycinate 400mg"],
            "avoid": ["Alcohol (disrupts REM sleep)", "Late heavy meals"]
        }
    
    def _get_quality_improvement_protocol(self) -> Dict[str, Any]:
        """Protocol for improving overall sleep quality."""
        return {
            "type": "quality_improvement",
            "steps": [
                {"time": "Morning", "action": "15 min sunlight exposure"},
                {"time": "Throughout day", "action": "No naps after 3 PM"},
                {"time": "Evening", "action": "Consistent wind-down routine"},
                {"time": "Bedtime", "action": "Same time every night (±30 min)"}
            ],
            "supplements": ["Magnesium glycinate 400mg"],
            "avoid": ["Irregular sleep schedule", "Weekend sleep-ins >1 hour"]
        }
    
    def _calculate_bedtime(self, wake_time: str, target_hours: float) -> str:
        """Calculate optimal bedtime based on wake time and target hours."""
        # Simplified - would use proper time calculation
        if target_hours == 7.5:
            return "11:30 PM"
        elif target_hours == 8:
            return "11:00 PM"
        else:
            return "10:30 PM"
    
    def _calculate_wind_down_time(self, bedtime: str) -> str:
        """Calculate when to start wind-down routine (1 hour before bed)."""
        # Simplified
        return "9:30 PM"
    
    def _generate_supporting_activities(
        self,
        energy_level: str,
        stress_level: str,
        sleep_quality: int
    ) -> Dict[str, Any]:
        """
        Generate supporting activities (30% focus).
        Light movement, nutrition timing, stress management.
        """
        return {
            "movement": {
                "type": "light",
                "recommendation": "20-minute morning walk (sunlight + movement improves sleep)",
                "timing": "Morning (within 1 hour of waking)",
                "avoid": "Intense exercise after 6 PM (can delay sleep onset)"
            },
            "nutrition": {
                "caffeine_cutoff": "2:00 PM",
                "last_meal": "3 hours before bed (7:30 PM if bedtime is 10:30 PM)",
                "sleep_supporting_foods": [
                    "Tart cherry juice (natural melatonin)",
                    "Almonds (magnesium)",
                    "Kiwi (serotonin precursor)"
                ],
                "avoid": ["Alcohol", "Spicy foods", "Large meals before bed"]
            },
            "stress_management": {
                "priority": "high" if stress_level in ["high", "very_high"] else "medium",
                "recommendation": "Stress disrupts sleep - manage throughout day",
                "techniques": [
                    "10-minute meditation (morning and evening)",
                    "Breathing exercises when stressed",
                    "Journaling before bed (brain dump)"
                ]
            }
        }
    
    def _get_intervention_priority(self, intervention_type: str) -> int:
        """
        Priority scores for sleep-focused users.
        Sleep interventions are highest priority.
        """
        priorities = {
            "sleep": 10,  # Highest - this is the primary goal
            "stress": 8,  # High - stress ruins sleep
            "recovery": 6,  # Medium - supports sleep
            "nutrition": 5,  # Supporting
            "barrier": 7  # High - removes obstacles
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
        Build sleep-focused morning briefing.
        """
        sleep_hours = biometrics.get("sleep_hours", 0)
        sleep_quality = biometrics.get("sleep_quality", 3)
        schedule = primary_focus["sleep_schedule"]
        
        briefing = f"Morning, {user_name}!\n\n"
        briefing += f"You slept {sleep_hours}h last night (target: {schedule['target_hours']}h)\n"
        
        if sleep_quality >= 4:
            briefing += f"✅ Sleep quality was excellent ({sleep_quality}/5)! Keep it up.\n\n"
        elif sleep_quality >= 3:
            briefing += f"Sleep quality was decent ({sleep_quality}/5). Let's improve tonight.\n\n"
        else:
            briefing += f"⚠️ Sleep quality was low ({sleep_quality}/5). Today's plan optimizes tonight.\n\n"
        
        briefing += "Today's sleep-supporting activities:\n"
        briefing += f"- {supporting_activities['movement']['recommendation']}\n"
        briefing += f"- Caffeine cutoff: {supporting_activities['nutrition']['caffeine_cutoff']}\n"
        briefing += f"- Wind-down starts: {schedule['wind_down_start']}\n"
        briefing += f"- Bedtime target: {schedule['target_bedtime']}\n"
        
        return briefing
    
    def _generate_tasks(
        self,
        primary_focus: Dict[str, Any],
        supporting_activities: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Generate actionable tasks for sleep-focused day.
        """
        schedule = primary_focus["sleep_schedule"]
        circadian = primary_focus["circadian_optimization"]
        
        return [
            {
                "time": "morning",
                "category": "circadian",
                "task": f"{circadian['morning_sunlight']['duration_minutes']} min morning sunlight walk",
                "priority": "critical"
            },
            {
                "time": "morning",
                "category": "movement",
                "task": supporting_activities["movement"]["recommendation"],
                "priority": "high"
            },
            {
                "time": supporting_activities["nutrition"]["caffeine_cutoff"],
                "category": "nutrition",
                "task": "Last call for caffeine (affects tonight's sleep)",
                "priority": "high"
            },
            {
                "time": "evening",
                "category": "nutrition",
                "task": f"Dinner by {supporting_activities['nutrition']['last_meal']}",
                "priority": "medium"
            },
            {
                "time": schedule["wind_down_start"],
                "category": "sleep_prep",
                "task": "Start wind-down routine (dim lights, no screens)",
                "priority": "critical"
            },
            {
                "time": schedule["target_bedtime"],
                "category": "sleep",
                "task": f"Bedtime - {primary_focus['tonight_protocol']['type']} protocol",
                "priority": "critical"
            }
        ]


# Singleton instance
sleep_daily_plan_generator = SleepDailyPlanGenerator()
