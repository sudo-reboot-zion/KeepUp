"""
Weekly Analysis Job
Aggregates weekly biometric data and generates insights
Shows contributing factors and causality analysis
Runs every Sunday night (or on demand)
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.models.resolution import Resolution
from backend.models.daily_checkin import DailyCheckIn
from backend.models.biometric_reading import BiometricReading
from backend.models.nutrition_entry import NutritionEntry
from backend.models.weekly_biometrics import WeeklyBiometrics
from backend.models.goal_progress import GoalProgress
from backend.models.baseline_metrics import BaselineMetrics
# from backend.services.opik_service import OpikLogger


class WeeklyAnalysisJob:
    """
    Aggregates weekly health data and generates insights.
    """
    
    def __init__(self, db: Session):
        self.db = db
        # self.opik = None  # Opik removed
    
    def run_weekly_analysis(self, resolution_id: int, week_number: int = None):
        """
        Analyze a specific week of data.
        If week_number not provided, analyze the most recent complete week.
        """
        if week_number is None:
            week_number = self._get_current_week_number()
        
        # Get week boundaries
        week_start, week_end = self._get_week_boundaries(week_number)
        
        # Aggregate biometric data
        biometric_agg = self._aggregate_biometrics(resolution_id, week_start, week_end)
        
        # Aggregate check-in data
        checkin_agg = self._aggregate_checkins(resolution_id, week_start, week_end)
        
        # Aggregate nutrition data
        nutrition_agg = self._aggregate_nutrition(resolution_id, week_start, week_end)
        
        # Create WeeklyBiometrics record
        weekly = self._create_weekly_biometrics(
            resolution_id, 
            week_number,
            week_start,
            week_end,
            biometric_agg
        )
        
        # Analyze contributing factors
        contributing_factors = self._analyze_contributing_factors(
            resolution_id,
            checkin_agg,
            nutrition_agg,
            biometric_agg,
            week_start,
            week_end
        )
        
        # Update GoalProgress with insights
        self._update_goal_progress_with_insights(
            resolution_id,
            biometric_agg,
            contributing_factors
        )
        
        return weekly
    
    def _get_current_week_number(self) -> int:
        """Get current week number (1-52)"""
        today = datetime.utcnow()
        return today.isocalendar()[1]
    
    def _get_week_boundaries(self, week_number: int, year: int = None) -> tuple:
        """Get start and end dates for a week"""
        if year is None:
            year = datetime.utcnow().year
        
        # Week 1 starts on Jan 1
        jan1 = datetime(year, 1, 1)
        
        # Calculate week start (Monday)
        week_start = jan1 + timedelta(weeks=week_number - 1)
        # Adjust to Monday
        week_start = week_start - timedelta(days=week_start.weekday())
        
        # Week end is Sunday
        week_end = week_start + timedelta(days=6, hours=23, minutes=59, seconds=59)
        
        return week_start, week_end
    
    def _aggregate_biometrics(
        self,
        resolution_id: int,
        week_start: datetime,
        week_end: datetime
    ) -> Dict:
        """
        Aggregate all biometric readings for the week.
        Calculate averages, min, max for each metric.
        """
        readings = self.db.query(BiometricReading).filter(
            BiometricReading.resolution_id == resolution_id,
            BiometricReading.date >= week_start,
            BiometricReading.date <= week_end
        ).all()
        
        agg = {
            "reading_count": len(readings),
            "bp_systolic": {"values": [], "avg": None, "min": None, "max": None},
            "bp_diastolic": {"values": [], "avg": None, "min": None, "max": None},
            "resting_hr": {"values": [], "avg": None, "min": None, "max": None},
            "weight_kg": {"values": [], "avg": None, "change": None},
        }
        
        for reading in readings:
            if reading.bp_systolic:
                agg["bp_systolic"]["values"].append(reading.bp_systolic)
            if reading.bp_diastolic:
                agg["bp_diastolic"]["values"].append(reading.bp_diastolic)
            if reading.resting_hr:
                agg["resting_hr"]["values"].append(reading.resting_hr)
            if reading.weight_kg:
                agg["weight_kg"]["values"].append(reading.weight_kg)
        
        # Calculate stats
        for metric in ["bp_systolic", "bp_diastolic", "resting_hr", "weight_kg"]:
            values = agg[metric]["values"]
            if values:
                agg[metric]["avg"] = sum(values) / len(values)
                agg[metric]["min"] = min(values)
                agg[metric]["max"] = max(values)
        
        # Calculate weight change
        if agg["weight_kg"]["values"]:
            agg["weight_kg"]["change"] = agg["weight_kg"]["values"][-1] - agg["weight_kg"]["values"][0]
        
        return agg
    
    def _aggregate_checkins(
        self,
        resolution_id: int,
        week_start: datetime,
        week_end: datetime
    ) -> Dict:
        """
        Aggregate daily check-in data for the week.
        Calculate averages for sleep, stress, mood.
        """
        checkins = self.db.query(DailyCheckIn).filter(
            DailyCheckIn.resolution_id == resolution_id,
            DailyCheckIn.date >= week_start,
            DailyCheckIn.date <= week_end
        ).all()
        
        agg = {
            "checkin_count": len(checkins),
            "sleep_hours": {"values": [], "avg": None},
            "stress_level": {"values": [], "avg": None},
            "mood": {},
            "energy_level": {"values": [], "avg": None},
            "symptoms_reported": [],
        }
        
        mood_counts = {}
        
        for checkin in checkins:
            if checkin.sleep_hours:
                agg["sleep_hours"]["values"].append(checkin.sleep_hours)
            if checkin.stress_level:
                agg["stress_level"]["values"].append(checkin.stress_level)
            if checkin.mood:
                mood_counts[checkin.mood] = mood_counts.get(checkin.mood, 0) + 1
            if checkin.energy_level:
                agg["energy_level"]["values"].append(checkin.energy_level)
            if checkin.symptoms:
                agg["symptoms_reported"].append(checkin.symptoms)
        
        # Calculate averages
        if agg["sleep_hours"]["values"]:
            agg["sleep_hours"]["avg"] = sum(agg["sleep_hours"]["values"]) / len(agg["sleep_hours"]["values"])
        if agg["stress_level"]["values"]:
            agg["stress_level"]["avg"] = sum(agg["stress_level"]["values"]) / len(agg["stress_level"]["values"])
        if agg["energy_level"]["values"]:
            agg["energy_level"]["avg"] = sum(agg["energy_level"]["values"]) / len(agg["energy_level"]["values"])
        
        # Most common mood
        if mood_counts:
            agg["mood"]["most_common"] = max(mood_counts, key=mood_counts.get)
            agg["mood"]["distribution"] = mood_counts
        
        return agg
    
    def _aggregate_nutrition(
        self,
        resolution_id: int,
        week_start: datetime,
        week_end: datetime
    ) -> Dict:
        """
        Aggregate nutrition data for the week.
        """
        entries = self.db.query(NutritionEntry).filter(
            NutritionEntry.resolution_id == resolution_id,
            NutritionEntry.date >= week_start,
            NutritionEntry.date <= week_end
        ).all()
        
        agg = {
            "entry_count": len(entries),
            "quality_rating": {"values": [], "avg": None},
            "categories": {},
            "on_track_count": 0,
        }
        
        for entry in entries:
            if entry.quality_rating:
                agg["quality_rating"]["values"].append(entry.quality_rating)
            if entry.quality_category:
                agg["categories"][entry.quality_category] = agg["categories"].get(entry.quality_category, 0) + 1
            if entry.on_track == "yes":
                agg["on_track_count"] += 1
        
        # Calculate average quality
        if agg["quality_rating"]["values"]:
            agg["quality_rating"]["avg"] = sum(agg["quality_rating"]["values"]) / len(agg["quality_rating"]["values"])
        
        return agg
    
    def _create_weekly_biometrics(
        self,
        resolution_id: int,
        week_number: int,
        week_start: datetime,
        week_end: datetime,
        biometric_agg: Dict
    ) -> WeeklyBiometrics:
        """
        Create or update WeeklyBiometrics record.
        """
        year = week_start.year
        
        # Check if already exists
        existing = self.db.query(WeeklyBiometrics).filter(
            WeeklyBiometrics.resolution_id == resolution_id,
            WeeklyBiometrics.week_number == week_number,
            WeeklyBiometrics.year == year
        ).first()
        
        if existing:
            # Update
            weekly = existing
        else:
            # Create new
            weekly = WeeklyBiometrics(
                resolution_id=resolution_id,
                week_number=week_number,
                year=year,
                week_start_date=week_start,
                week_end_date=week_end,
            )
            self.db.add(weekly)
        
        # Update values
        weekly.avg_bp_systolic = int(biometric_agg["bp_systolic"]["avg"]) if biometric_agg["bp_systolic"]["avg"] else None
        weekly.avg_bp_diastolic = int(biometric_agg["bp_diastolic"]["avg"]) if biometric_agg["bp_diastolic"]["avg"] else None
        weekly.min_bp_systolic = biometric_agg["bp_systolic"]["min"]
        weekly.max_bp_systolic = biometric_agg["bp_systolic"]["max"]
        weekly.avg_resting_hr = int(biometric_agg["resting_hr"]["avg"]) if biometric_agg["resting_hr"]["avg"] else None
        weekly.avg_weight_kg = biometric_agg["weight_kg"]["avg"]
        weekly.weight_change_from_baseline = biometric_agg["weight_kg"]["change"]
        weekly.avg_waist_circumference_cm = None  # TODO: Add if available
        weekly.bp_reading_count = len(biometric_agg["bp_systolic"]["values"])
        weekly.weight_reading_count = len(biometric_agg["weight_kg"]["values"])
        
        # Determine trend (compare to previous week)
        trend = self._analyze_trend(resolution_id, week_number, biometric_agg)
        weekly.trend_direction = trend["direction"]
        weekly.trend_strength = trend["strength"]
        
        self.db.commit()
        self.db.refresh(weekly)
        
        return weekly
    
    def _analyze_trend(
        self,
        resolution_id: int,
        week_number: int,
        biometric_agg: Dict
    ) -> Dict:
        """
        Compare this week to previous week to determine trend.
        """
        # Get previous week
        prev_week = self.db.query(WeeklyBiometrics).filter(
            WeeklyBiometrics.resolution_id == resolution_id,
            WeeklyBiometrics.week_number == week_number - 1
        ).first()
        
        if not prev_week or not prev_week.avg_weight_kg:
            return {"direction": "stable", "strength": "no_data"}
        
        current_weight = biometric_agg["weight_kg"]["avg"]
        prev_weight = prev_week.avg_weight_kg
        
        if not current_weight:
            return {"direction": "stable", "strength": "no_data"}
        
        change = current_weight - prev_weight
        
        if change <= -0.5:
            return {"direction": "improving", "strength": "strong"}
        elif change < 0:
            return {"direction": "improving", "strength": "moderate"}
        elif change == 0:
            return {"direction": "stable", "strength": "no_change"}
        elif change < 0.5:
            return {"direction": "declining", "strength": "weak"}
        else:
            return {"direction": "declining", "strength": "strong"}
    
    def _analyze_contributing_factors(
        self,
        resolution_id: int,
        checkin_agg: Dict,
        nutrition_agg: Dict,
        biometric_agg: Dict,
        week_start: datetime,
        week_end: datetime
    ) -> List[str]:
        """
        Analyze what contributed to health improvements or declines.
        """
        factors = []
        
        # Sleep impact
        if checkin_agg["sleep_hours"]["avg"]:
            if checkin_agg["sleep_hours"]["avg"] >= 8:
                factors.append(f"Excellent sleep ({checkin_agg['sleep_hours']['avg']:.1f}h/night)")
            elif checkin_agg["sleep_hours"]["avg"] >= 7:
                factors.append(f"Good sleep ({checkin_agg['sleep_hours']['avg']:.1f}h/night)")
            elif checkin_agg["sleep_hours"]["avg"] < 6:
                factors.append(f"Poor sleep ({checkin_agg['sleep_hours']['avg']:.1f}h/night)")
        
        # Stress impact
        if checkin_agg["stress_level"]["avg"]:
            if checkin_agg["stress_level"]["avg"] >= 7:
                factors.append(f"High stress ({checkin_agg['stress_level']['avg']:.0f}/10)")
            elif checkin_agg["stress_level"]["avg"] <= 3:
                factors.append(f"Low stress ({checkin_agg['stress_level']['avg']:.0f}/10)")
        
        # Nutrition impact
        if nutrition_agg["quality_rating"]["avg"]:
            if nutrition_agg["quality_rating"]["avg"] >= 8:
                factors.append(f"Excellent nutrition quality ({nutrition_agg['quality_rating']['avg']:.0f}/10)")
            elif nutrition_agg["quality_rating"]["avg"] >= 7:
                factors.append(f"Good nutrition ({nutrition_agg['quality_rating']['avg']:.0f}/10)")
            elif nutrition_agg["quality_rating"]["avg"] <= 3:
                factors.append(f"Poor nutrition ({nutrition_agg['quality_rating']['avg']:.0f}/10)")
        
        # Activity/workouts (TODO: count actual workouts)
        # factors.append(f"3 workouts completed")
        
        return factors
    
    def _update_goal_progress_with_insights(
        self,
        resolution_id: int,
        biometric_agg: Dict,
        contributing_factors: List[str]
    ):
        """
        Update GoalProgress records with weekly insights.
        """
        # Update BP progress
        if biometric_agg["bp_systolic"]["avg"]:
            progress = self.db.query(GoalProgress).filter(
                GoalProgress.resolution_id == resolution_id,
                GoalProgress.metric_type == "blood_pressure"
            ).first()
            
            if progress:
                progress.current_value = biometric_agg["bp_systolic"]["avg"]
                progress.contributing_factors = ", ".join(contributing_factors)
                
                # Generate insight
                if biometric_agg["bp_systolic"]["avg"] < progress.baseline_value:
                    improvement = progress.baseline_value - biometric_agg["bp_systolic"]["avg"]
                    progress.insight_text = f"BP improved by {improvement:.0f} points. Key contributors: {', '.join(contributing_factors[:2])}"
                
                self.db.commit()
        
        # Update weight progress
        if biometric_agg["weight_kg"]["avg"]:
            progress = self.db.query(GoalProgress).filter(
                GoalProgress.resolution_id == resolution_id,
                GoalProgress.metric_type == "weight"
            ).first()
            
            if progress:
                progress.current_value = biometric_agg["weight_kg"]["avg"]
                progress.contributing_factors = ", ".join(contributing_factors)
                
                if biometric_agg["weight_kg"]["change"]:
                    progress.insight_text = f"Weight changed by {biometric_agg['weight_kg']['change']:.1f}kg this week. Factors: {', '.join(contributing_factors[:2])}"
                
                self.db.commit()
