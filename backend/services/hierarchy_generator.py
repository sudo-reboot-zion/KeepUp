"""
Resolution Hierarchy Generator
Generates Quarters, Weeks, and Daily Workouts for a 52-week resolution
"""
from datetime import datetime, timedelta
from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from models.resolution import Resolution
from models.quarterly_phase import QuarterlyPhase, QuarterNumber
from models.weekly_plan import WeeklyPlan, WeeklyStatus
from models.daily_workout import DailyWorkout, DayOfWeek, WorkoutStatus

class ResolutionHierarchyGenerator:
    """Generates the full 52-week hierarchy for a resolution"""
    
    @staticmethod
    async def generate_hierarchy(resolution: Resolution, db: AsyncSession) -> Dict[str, Any]:
        """
        Generate 4 quarters, 52 weeks, and placeholder workouts
        """
        print(f"Generating hierarchy for resolution {resolution.id}...")
        
        # 1. Define Quarters
        quarters_data = [
            {
                "number": QuarterNumber.Q1,
                "name": "Foundation",
                "description": "Building consistency and habit formation",
                "weeks": range(1, 14),
                "focus": ["habit_formation", "consistency", "routine"]
            },
            {
                "number": QuarterNumber.Q2,
                "name": "Progression",
                "description": "Increasing intensity and volume",
                "weeks": range(14, 27),
                "focus": ["intensity", "stamina", "variation"]
            },
            {
                "number": QuarterNumber.Q3,
                "name": "Mastery",
                "description": "Building endurance and managing plateaus",
                "weeks": range(27, 40),
                "focus": ["endurance", "skill_refinement", "resilience"]
            },
            {
                "number": QuarterNumber.Q4,
                "name": "Acceleration",
                "description": "Final push towards peak performance",
                "weeks": range(40, 53),
                "focus": ["peak_performance", "goal_achievement", "legacy"]
            }
        ]
        
        total_weeks = 0
        total_workouts = 0
        
        # Current date for starting point
        start_date = resolution.created_at or datetime.utcnow()
        # Align to next Monday
        days_ahead = 7 - start_date.weekday()
        if days_ahead == 7: days_ahead = 0
        current_monday = (start_date + timedelta(days=days_ahead)).replace(hour=0, minute=0, second=0, microsecond=0)
        
        for q_data in quarters_data:
            # Create Quarter
            quarter = QuarterlyPhase(
                resolution_id=resolution.id,
                quarter=q_data["number"],
                week_start=q_data["weeks"].start,
                week_end=q_data["weeks"].stop - 1,
                phase_name=q_data["name"],
                phase_description=q_data["description"],
                focus_areas=q_data["focus"],
                target_workouts=len(q_data["weeks"]) * (resolution.workouts_target or 3),
                milestones=[],
                risk_factors=["plateau", "life_events"],
                protective_strategies=["early_intervention"]
            )
            db.add(quarter)
            await db.flush() # Get quarter ID
            
            # Create Weeks for this quarter
            for week_idx, global_week in enumerate(q_data["weeks"]):
                week_start_date = current_monday + timedelta(weeks=global_week - 1)
                week_end_date = week_start_date + timedelta(days=6, hours=23, minutes=59)
                
                week_plan = WeeklyPlan(
                    quarterly_phase_id=quarter.id,
                    resolution_id=resolution.id,
                    week_number=global_week,
                    quarter_week=week_idx + 1,
                    week_start_date=week_start_date,
                    week_end_date=week_end_date,
                    target_workouts=resolution.workouts_target or 3,
                    target_duration_minutes=90, # Placeholder
                    focus=q_data["name"],
                    estimated_difficulty="moderate",
                    risk_level="low",
                    protective_measures=[],
                    status=WeeklyStatus.IN_PROGRESS if global_week == resolution.current_week else WeeklyStatus.UPCOMING
                )
                db.add(week_plan)
                await db.flush() # Get week ID
                total_weeks += 1
                
                # Create default Workout placeholders for Mon, Wed, Fri
                workout_days = [
                    (DayOfWeek.MONDAY, 0),
                    (DayOfWeek.WEDNESDAY, 2),
                    (DayOfWeek.FRIDAY, 4)
                ]
                
                for day_name, offset in workout_days:
                    workout_date = week_start_date + timedelta(days=offset)
                    workout = DailyWorkout(
                        weekly_plan_id=week_plan.id,
                        resolution_id=resolution.id,
                        date=workout_date,
                        day_of_week=day_name,
                        planned_workout_type="Foundation Session",
                        planned_duration_minutes=30,
                        planned_exercises=[{"name": "Initial Training", "sets": 3, "reps": 10}],
                        planned_intensity="moderate",
                        status=WorkoutStatus.SCHEDULED
                    )
                    db.add(workout)
                    total_workouts += 1
        
        await db.commit()
        return {
            "total_weeks": total_weeks,
            "total_workouts": total_workouts
        }
