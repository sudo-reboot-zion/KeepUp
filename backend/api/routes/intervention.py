"""
Intervention API Routes
Provides active interventions for users
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from datetime import date

from core.database import get_db
from api.dependencies import get_current_user
from models.user import User
from models.daily_log import UserDailyLog


router = APIRouter(prefix="/intervention", tags=["Intervention"])


@router.get("/active")
async def get_active_interventions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get active interventions for the current user based on today's check-in
    """
    try:
        # Get today's check-in
        today = date.today()
        checkin_query = select(UserDailyLog).where(
            and_(
                UserDailyLog.user_id == current_user.id,
                UserDailyLog.date == today
            )
        )
        checkin_result = await db.execute(checkin_query)
        checkin = checkin_result.scalar_one_or_none()
        
        if not checkin:
            return {"interventions": []}
        
        interventions = []
        
        # Check for poor sleep
        if checkin.sleep_quality and checkin.sleep_quality < 3:
            interventions.append({
                "type": "sleep",
                "severity": "high" if checkin.sleep_quality < 2 else "medium",
                "recommendation": "Your sleep quality is below optimal. Prioritize rest tonight.",
                "actions": [
                    "Aim for 8 hours of sleep tonight",
                    "Avoid caffeine after 2 PM",
                    "Create a relaxing bedtime routine",
                    "Consider reducing workout intensity today"
                ]
            })
        
        # Check for high stress
        if checkin.stress_level and checkin.stress_level.value in ["high", "very_high"]:
            interventions.append({
                "type": "stress",
                "severity": "high" if checkin.stress_level.value == "very_high" else "medium",
                "recommendation": "Your stress levels are elevated. Take time for stress management.",
                "actions": [
                    "Practice 10 minutes of meditation",
                    "Take short breaks throughout the day",
                    "Try deep breathing exercises",
                    "Consider a lighter workout today"
                ]
            })
        
        # Check for high soreness
        if checkin.soreness_level and checkin.soreness_level.value in ["high", "severe"]:
            interventions.append({
                "type": "recovery",
                "severity": "high" if checkin.soreness_level.value == "severe" else "medium",
                "recommendation": "Your body needs recovery. Focus on active recovery today.",
                "actions": [
                    "Light stretching or yoga",
                    "Foam rolling",
                    "Low-intensity cardio only",
                    "Ensure adequate protein intake"
                ]
            })
        
        # Check for low energy
        if checkin.energy_level and checkin.energy_level.value in ["very_low", "low"]:
            interventions.append({
                "type": "nutrition",
                "severity": "medium",
                "recommendation": "Your energy is low. Focus on nutrition and hydration.",
                "actions": [
                    "Eat a balanced breakfast",
                    "Stay hydrated (8+ glasses of water)",
                    "Include complex carbs in meals",
                    "Avoid excessive caffeine"
                ]
            })
        
        return {"interventions": interventions}
        
    except Exception as e:
        print(f"Error getting interventions: {e}")
        return {"interventions": []}
