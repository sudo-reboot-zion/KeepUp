"""
Adaptive Recommendation Service
Orchestrates agent decision-making based on multi-factor health inputs
Generates adaptive workout recommendations, recovery suggestions, etc
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from agents.adaptive_intervention.nutrition_pivot_agent import NutritionPivotAgent
from sqlalchemy.orm import Session
import json

from models.resolution import Resolution
from models.daily_checkin import DailyCheckIn
from models.biometric_reading import BiometricReading
from models.baseline_metrics import BaselineMetrics
from models.agent_recommendation import AgentRecommendation
from models.agent_decision import AgentDecision
from models.goal_progress import GoalProgress
from models.nutrition_entry import NutritionEntry

# Import agents
from agents.mental_wellness.emotional_support_agent import EmotionalSupportAgent
# from agents.task_management.task_generation_agent import TaskGenerationAgent

from agents.biometric_environment.biometric_agent import BiometricAgent


# # from evaluation.opik_logger import OpikLogger


class AdaptiveRecommendationService:
    """
    Core service for generating adaptive recommendations.
    Analyzes user data and coordinates multiple agents to decide
    the best action for the user on a given day.
    """
    
    def __init__(self, db: Session):
        self.db = db
        # self.opik_logger = None  # Opik removed
        # Agents commented out - need to be properly imported/defined
        # self.emotional_agent = EmotionalAgent()
        # self.task_agent = TaskManagementAgent()
        # self.resolution_agent = ResolutionTrackingAgent()
        # self.biometric_agent = BiometricEnvironmentAgent()
        self.nutrition_agent = NutritionPivotAgent()
    
    
    def generate_recommendation(
        self,
        resolution_id: int,
        daily_checkin_id: int,
        user_id: int
    ) -> AgentRecommendation:
        """
        Main orchestration function.
        Takes user's daily check-in and generates recommendation.
        """
        # 1. Fetch all context
        context = self._build_context(resolution_id, user_id)
        
        # 2. Analyze with agents
        analyses = self._run_agent_analyses(resolution_id, context)
        
        # 3. Synthesize decision
        recommendation = self._synthesize_recommendation(
            resolution_id,
            daily_checkin_id,
            context,
            analyses
        )
        
        # 4. Log to database
        self.db.add(recommendation)
        self.db.commit()
        self.db.refresh(recommendation)
        
        return recommendation
    
    def _build_context(self, resolution_id: int, user_id: int) -> Dict:
        """
        Gather all relevant context for decision-making.
        """
        # Latest check-in
        latest_checkin = self.db.query(DailyCheckIn).filter(
            DailyCheckIn.resolution_id == resolution_id,
            DailyCheckIn.user_id == user_id
        ).order_by(DailyCheckIn.date.desc()).first()
        
        # Last 7 days of check-ins for trends
        week_ago = datetime.utcnow() - timedelta(days=7)
        week_checkins = self.db.query(DailyCheckIn).filter(
            DailyCheckIn.resolution_id == resolution_id,
            DailyCheckIn.user_id == user_id,
            DailyCheckIn.date >= week_ago
        ).all()
        
        # Latest biometrics
        latest_biometric = self.db.query(BiometricReading).filter(
            BiometricReading.resolution_id == resolution_id,
            BiometricReading.user_id == user_id
        ).order_by(BiometricReading.date.desc()).first()
        
        # Baseline metrics
        baseline = self.db.query(BaselineMetrics).filter(
            BaselineMetrics.resolution_id == resolution_id
        ).first()
        
        # Recent nutrition
        recent_nutrition = self.db.query(NutritionEntry).filter(
            NutritionEntry.resolution_id == resolution_id,
            NutritionEntry.user_id == user_id,
            NutritionEntry.date >= week_ago
        ).all()
        
        # Resolution info
        resolution = self.db.query(Resolution).filter(
            Resolution.id == resolution_id
        ).first()
        
        # Recent workouts (from daily workout model if available)
        recent_workouts = 2  # TODO: Query actual workouts
        
        context = {
            "latest_checkin": {
                "sleep_hours": latest_checkin.sleep_hours if latest_checkin else None,
                "stress_level": latest_checkin.stress_level if latest_checkin else None,
                "mood": latest_checkin.mood if latest_checkin else None,
                "energy_level": latest_checkin.energy_level if latest_checkin else None,
                "symptoms": latest_checkin.symptoms if latest_checkin else None,
            },
            "week_trends": {
                "avg_sleep_hours": sum([c.sleep_hours for c in week_checkins if c.sleep_hours]) / max(len([c for c in week_checkins if c.sleep_hours]), 1),
                "avg_stress_level": sum([c.stress_level for c in week_checkins if c.stress_level]) / max(len([c for c in week_checkins if c.stress_level]), 1),
                "checkins_completed": len(week_checkins),
            },
            "latest_biometric": {
                "bp_systolic": latest_biometric.bp_systolic if latest_biometric else baseline.bp_systolic_baseline if baseline else None,
                "bp_diastolic": latest_biometric.bp_diastolic if latest_biometric else baseline.bp_diastolic_baseline if baseline else None,
                "resting_hr": latest_biometric.resting_hr if latest_biometric else baseline.resting_hr_baseline if baseline else None,
                "weight_kg": latest_biometric.weight_kg if latest_biometric else baseline.weight_baseline_kg if baseline else None,
            },
            "baseline": {
                "bp_systolic": baseline.bp_systolic_baseline if baseline else None,
                "bp_diastolic": baseline.bp_diastolic_baseline if baseline else None,
                "weight_target_kg": baseline.weight_target_kg if baseline else None,
                "resting_hr_target": baseline.resting_hr_target if baseline else None,
            },
            "nutrition": {
                "entries_this_week": len(recent_nutrition),
                "avg_quality_rating": sum([n.quality_rating for n in recent_nutrition if n.quality_rating]) / max(len([n for n in recent_nutrition if n.quality_rating]), 1),
            },
            "goal": resolution.resolution_text if resolution else None,
            "recent_workouts": recent_workouts,
        }
        
        return context
    
    def _run_agent_analyses(self, resolution_id: int, context: Dict) -> Dict:
        """
        Run all relevant agents to analyze situation.
        Each agent provides insights in their domain.
        """
        analyses = {}
        
        # 1. Emotional Agent: Is user burned out?
        try:
            emotional_analysis = self.emotional_agent.analyze(
                stress_level=context["latest_checkin"]["stress_level"],
                sleep_hours=context["latest_checkin"]["sleep_hours"],
                mood=context["latest_checkin"]["mood"],
                energy_level=context["latest_checkin"]["energy_level"],
                week_trend_sleep=context["week_trends"]["avg_sleep_hours"],
                week_trend_stress=context["week_trends"]["avg_stress_level"],
            )
            analyses["emotional"] = emotional_analysis
        except Exception as e:
            analyses["emotional"] = {"error": str(e), "burnout_risk": "unknown"}
        
        # 2. Task Management Agent: Should we adapt workout?
        try:
            task_analysis = self.task_agent.analyze(
                sleep_hours=context["latest_checkin"]["sleep_hours"],
                stress_level=context["latest_checkin"]["stress_level"],
                energy_level=context["latest_checkin"]["energy_level"],
                recent_workouts=context["recent_workouts"],
                goal=context["goal"],
            )
            analyses["task"] = task_analysis
        except Exception as e:
            analyses["task"] = {"error": str(e), "recommendation": "normal"}
        
        # 3. Resolution Tracking Agent: How's goal progress?
        try:
            resolution_analysis = self.resolution_agent.analyze(
                current_bp=context["latest_biometric"]["bp_systolic"],
                baseline_bp=context["baseline"]["bp_systolic"],
                current_weight=context["latest_biometric"]["weight_kg"],
                baseline_weight=context["baseline"]["weight_target_kg"],
                workouts_completed=context["recent_workouts"],
                goal=context["goal"],
            )
            analyses["resolution"] = resolution_analysis
        except Exception as e:
            analyses["resolution"] = {"error": str(e), "progress": "unknown"}
        
        # 4. Biometric Environment Agent: What do readings mean?
        try:
            biometric_analysis = self.biometric_agent.analyze(
                bp_systolic=context["latest_biometric"]["bp_systolic"],
                bp_diastolic=context["latest_biometric"]["bp_diastolic"],
                resting_hr=context["latest_biometric"]["resting_hr"],
                baseline_bp=context["baseline"]["bp_systolic"],
                baseline_hr=context["baseline"]["resting_hr_target"],
            )
            analyses["biometric"] = biometric_analysis
        except Exception as e:
            analyses["biometric"] = {"error": str(e), "status": "unknown"}
        
        # 5. Nutrition Agent: How's nutrition affecting goal?
        try:
            nutrition_analysis = self.nutrition_agent.analyze(
                nutrition_quality=context["nutrition"]["avg_quality_rating"],
                entries_this_week=context["nutrition"]["entries_this_week"],
                goal=context["goal"],
                bp_change=context["latest_biometric"]["bp_systolic"] - context["baseline"]["bp_systolic"] if context["baseline"]["bp_systolic"] else 0,
            )
            analyses["nutrition"] = nutrition_analysis
        except Exception as e:
            analyses["nutrition"] = {"error": str(e), "recommendation": "neutral"}
        
        return analyses
    
    def _synthesize_recommendation(
        self,
        resolution_id: int,
        daily_checkin_id: int,
        context: Dict,
        analyses: Dict
    ) -> AgentRecommendation:
        """
        Synthesize all agent analyses into single recommendation.
        Determines: workout type, intensity, reasoning, confidence.
        """
        
        # Extract key signals
        sleep_hours = context["latest_checkin"]["sleep_hours"] or 7
        stress_level = context["latest_checkin"]["stress_level"] or 5
        energy_level = context["latest_checkin"]["energy_level"] or 5
        
        # Decision logic
        recommendation_type = "normal"  # default
        recommended_intensity = "moderate"
        recommended_workout_type = "strength"
        recommended_duration = 60
        confidence_score = 0.7
        supporting_factors = []
        reasoning_parts = []
        
        # Rule 1: Low sleep → recovery focus
        if sleep_hours < 6:
            recommendation_type = "recovery_focus"
            recommended_intensity = "light"
            recommended_workout_type = "mobility"
            recommended_duration = 20
            confidence_score = 0.9
            supporting_factors.append("low_sleep")
            reasoning_parts.append(f"Sleep only {sleep_hours}h - body needs recovery")
        
        # Rule 2: High stress + low energy → skip
        elif stress_level >= 8 and energy_level <= 4:
            recommendation_type = "skip_workout"
            recommended_workout_type = "rest"
            recommended_duration = 0
            confidence_score = 0.85
            supporting_factors.append("high_stress")
            supporting_factors.append("low_energy")
            reasoning_parts.append(f"High stress ({stress_level}/10) + low energy ({energy_level}/10) = skip for recovery")
        
        # Rule 3: High stress but okay energy → reduce intensity
        elif stress_level >= 7 and energy_level >= 5:
            recommendation_type = "reduce_intensity"
            recommended_intensity = "light"
            recommended_duration = 30
            confidence_score = 0.8
            supporting_factors.append("elevated_stress")
            reasoning_parts.append(f"Stress high ({stress_level}/10) - reduce intensity to manage cortisol")
        
        # Rule 4: Good sleep + good energy → push
        elif sleep_hours >= 8 and energy_level >= 8:
            recommendation_type = "push_harder"
            recommended_intensity = "high"
            recommended_workout_type = "strength"
            recommended_duration = 90
            confidence_score = 0.85
            supporting_factors.append("good_sleep")
            supporting_factors.append("high_energy")
            reasoning_parts.append(f"Great sleep ({sleep_hours}h) + high energy ({energy_level}/10) - optimal for strength")
        
        # Rule 5: Check nutrition impact
        nutrition_avg = context["nutrition"]["avg_quality_rating"] or 5
        if nutrition_avg >= 8:
            supporting_factors.append("good_nutrition")
            reasoning_parts.append(f"Nutrition on track (quality: {nutrition_avg}/10)")
            confidence_score = min(confidence_score + 0.05, 1.0)
        elif nutrition_avg <= 3:
            supporting_factors.append("poor_nutrition")
            reasoning_parts.append(f"Nutrition poor (quality: {nutrition_avg}/10)")
            if recommendation_type == "normal":
                recommendation_type = "reduce_intensity"
                confidence_score = min(confidence_score + 0.1, 1.0)
        
        # Rule 6: Check biometric trends
        bp_change = (context["latest_biometric"]["bp_systolic"] or 0) - (context["baseline"]["bp_systolic"] or 0)
        if bp_change <= -5:
            supporting_factors.append("good_bp_progress")
            reasoning_parts.append(f"BP improved {abs(bp_change)}pts - maintain current approach")
            confidence_score = min(confidence_score + 0.1, 1.0)
        elif bp_change >= 5:
            supporting_factors.append("rising_bp")
            reasoning_parts.append(f"BP elevated {bp_change}pts - increase recovery focus")
            confidence_score = min(confidence_score + 0.1, 1.0)
        
        # Create recommendation object
        recommendation = AgentRecommendation(
            resolution_id=resolution_id,
            daily_checkin_id=daily_checkin_id,
            recommendation_type=recommendation_type,
            recommendation_text=f"{recommendation_type.replace('_', ' ').title()}: {recommended_duration}min {recommended_intensity} {recommended_workout_type}",
            reasoning=". ".join(reasoning_parts) if reasoning_parts else "Balanced approach based on current metrics",
            agent_name="adaptive_recommendation_service",
            agent_type="ensemble",
            confidence_score=confidence_score,
            supporting_factors=",".join(supporting_factors),
            recommended_workout_type=recommended_workout_type,
            recommended_duration_minutes=recommended_duration,
            recommended_intensity=recommended_intensity,
            date=datetime.utcnow(),
        )
        
        
        # Opik logging removed
        # try:
        #     opik_trace_id = self.opik_logger.log_recommendation(
        #         resolution_id=resolution_id,
        #         context=context,
        #         analyses=analyses,
        #         recommendation=recommendation
        #     )
        #     recommendation.opik_trace_id = opik_trace_id
        # except Exception as e:
        #     print(f"Warning: Opik logging failed: {e}")
        
        return recommendation
    
    def update_goal_progress(
        self,
        resolution_id: int,
        metric_type: str,
        current_value: float
    ) -> Optional[GoalProgress]:
        """
        Update goal progress after new biometric reading.
        Calculate trends, % progress, and days to goal.
        """
        baseline = self.db.query(BaselineMetrics).filter(
            BaselineMetrics.resolution_id == resolution_id
        ).first()
        
        if not baseline:
            return None
        
        # Determine baseline and target from metric type
        if metric_type == "blood_pressure":
            baseline_value = baseline.bp_systolic_baseline
            target_value = baseline.bp_systolic_target
            metric_unit = "mmHg"
        elif metric_type == "weight":
            baseline_value = baseline.weight_baseline_kg
            target_value = baseline.weight_target_kg
            metric_unit = "kg"
        elif metric_type == "resting_hr":
            baseline_value = baseline.resting_hr_baseline
            target_value = baseline.resting_hr_target
            metric_unit = "bpm"
        else:
            return None
        
        if not baseline_value or not target_value:
            return None
        
        # Get or create GoalProgress
        progress = self.db.query(GoalProgress).filter(
            GoalProgress.resolution_id == resolution_id,
            GoalProgress.metric_type == metric_type
        ).first()
        
        if not progress:
            progress = GoalProgress(
                resolution_id=resolution_id,
                baseline_metrics_id=baseline.id,
                metric_type=metric_type,
                metric_unit=metric_unit,
                baseline_value=baseline_value,
                target_value=target_value,
                days_elapsed=0,
            )
            self.db.add(progress)
        
        # Update current value
        progress.current_value = current_value
        progress.last_measurement_date = datetime.utcnow()
        
        # Calculate change
        value_change = current_value - baseline_value
        progress.value_change = value_change
        
        # Calculate % progress
        total_change_needed = target_value - baseline_value
        if total_change_needed != 0:
            percentage = (value_change / total_change_needed) * 100
            progress.percentage_progress = min(percentage, 100)
        
        # Estimate days to goal
        # Get recent readings to calculate rate of change
        biometrics = self.db.query(BiometricReading).filter(
            BiometricReading.resolution_id == resolution_id
        ).order_by(BiometricReading.date.desc()).limit(10).all()
        
        if len(biometrics) >= 2:
            first_date = biometrics[-1].date
            latest_date = biometrics[0].date
            days_elapsed = (latest_date - first_date).days
            
            if days_elapsed > 0:
                # Get relevant field for metric
                if metric_type == "blood_pressure":
                    first_value = biometrics[-1].bp_systolic
                    latest_value = biometrics[0].bp_systolic
                elif metric_type == "weight":
                    first_value = biometrics[-1].weight_kg
                    latest_value = biometrics[0].weight_kg
                else:
                    first_value = latest_value = None
                
                if first_value and latest_value:
                    change_per_day = (latest_value - first_value) / days_elapsed
                    if change_per_day != 0:
                        days_remaining = int(abs((target_value - current_value) / change_per_day))
                        progress.days_to_goal_estimate = days_remaining
        
        # Determine trend
        if progress.percentage_progress is not None:
            if progress.percentage_progress > 50:
                progress.trend_direction = "improving"
                progress.trend_strength = "strong"
            elif progress.percentage_progress > 20:
                progress.trend_direction = "improving"
                progress.trend_strength = "moderate"
            elif progress.percentage_progress > 0:
                progress.trend_direction = "improving"
                progress.trend_strength = "weak"
            elif progress.percentage_progress == 0:
                progress.trend_direction = "stable"
            else:
                progress.trend_direction = "declining"
        
        self.db.commit()
        self.db.refresh(progress)
        
        return progress
