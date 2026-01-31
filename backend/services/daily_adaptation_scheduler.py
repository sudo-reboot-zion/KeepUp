"""
Daily Adaptation Scheduler
Generates daily adaptive workout recommendations based on previous day's check-in
Runs every morning at 7 AM (configurable)
"""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from typing import Optional

from backend.models.resolution import Resolution
from backend.models.daily_checkin import DailyCheckIn
from backend.models.daily_workout import DailyWorkout
from backend.services.adaptive_recommendation_service import AdaptiveRecommendationService


class DailyAdaptationScheduler:
    """
    Runs daily to generate adapted workout recommendations.
    Called every morning - analyzes yesterday's check-in and recommends today's workout.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.rec_service = AdaptiveRecommendationService(db)
    
    def generate_daily_adaptations(self):
        """
        Main job that runs daily.
        For each active resolution, generate today's adapted recommendation.
        """
        # Get all active resolutions
        active_resolutions = self.db.query(Resolution).filter(
            Resolution.status == "active"
        ).all()
        
        for resolution in active_resolutions:
            try:
                self._adapt_for_resolution(resolution)
            except Exception as e:
                print(f"Error adapting resolution {resolution.id}: {e}")
    
    def _adapt_for_resolution(self, resolution: Resolution):
        """
        Generate adapted recommendation for a specific resolution.
        """
        # Get yesterday's check-in
        yesterday = datetime.utcnow() - timedelta(days=1)
        yesterday_start = yesterday.replace(hour=0, minute=0, second=0)
        yesterday_end = yesterday.replace(hour=23, minute=59, second=59)
        
        yesterday_checkin = self.db.query(DailyCheckIn).filter(
            DailyCheckIn.resolution_id == resolution.id,
            DailyCheckIn.date >= yesterday_start,
            DailyCheckIn.date <= yesterday_end
        ).first()
        
        # If no check-in yesterday, use default recommendation
        if not yesterday_checkin:
            return self._create_default_workout(resolution)
        
        # Generate adapted recommendation based on yesterday's data
        recommendation = self.rec_service.generate_recommendation(
            resolution_id=resolution.id,
            daily_checkin_id=yesterday_checkin.id,
            user_id=resolution.user_id
        )
        
        # Create or update today's DailyWorkout with the adapted recommendation
        today = datetime.utcnow().date()
        today_start = datetime.combine(today, datetime.min.time())
        
        workout = self.db.query(DailyWorkout).filter(
            DailyWorkout.resolution_id == resolution.id,
            DailyWorkout.date >= today_start
        ).first()
        
        if workout:
            # Update existing
            workout.adapted_recommendation = recommendation.recommendation_text
            workout.adapted_intensity = recommendation.recommended_intensity
            workout.adapted_type = recommendation.recommended_workout_type
            workout.adaptation_reason = recommendation.reasoning
            workout.agent_confidence_score = recommendation.confidence_score
        else:
            # Create new (shouldn't happen if hierarchy generator works)
            # But create as fallback
            workout = DailyWorkout(
                resolution_id=resolution.id,
                date=today_start,
                week_number=self._get_week_number(today),
                day_of_week=today.weekday(),
                planned_type=recommendation.recommended_workout_type,
                planned_duration_minutes=recommendation.recommended_duration_minutes,
                planned_intensity=recommendation.recommended_intensity,
                adapted_recommendation=recommendation.recommendation_text,
                adapted_intensity=recommendation.recommended_intensity,
                adapted_type=recommendation.recommended_workout_type,
                adaptation_reason=recommendation.reasoning,
                agent_confidence_score=recommendation.confidence_score,
            )
            self.db.add(workout)
        
        self.db.commit()
    
    def _create_default_workout(self, resolution: Resolution) -> DailyWorkout:
        """
        Create default workout for a day when no check-in data is available.
        """
        today = datetime.utcnow().date()
        today_start = datetime.combine(today, datetime.min.time())
        
        # Check if today is a planned workout day
        day_of_week = today.weekday()
        
        # Default: Mon/Wed/Fri workouts
        if day_of_week in [0, 2, 4]:  # Monday, Wednesday, Friday
            planned_type = "strength"
            duration = 60
            intensity = "moderate"
        else:
            planned_type = "rest"
            duration = 0
            intensity = "light"
        
        workout = DailyWorkout(
            resolution_id=resolution.id,
            date=today_start,
            week_number=self._get_week_number(today),
            day_of_week=day_of_week,
            planned_type=planned_type,
            planned_duration_minutes=duration,
            planned_intensity=intensity,
            adapted_recommendation=f"Default: {planned_type}",
            adapted_intensity=intensity,
            adapted_type=planned_type,
            adaptation_reason="No check-in data available, using default schedule",
            agent_confidence_score=0.5,
        )
        
        self.db.add(workout)
        self.db.commit()
        
        return workout
    
    def _get_week_number(self, date) -> int:
        """Get week number (1-52)"""
        return date.isocalendar()[1]
