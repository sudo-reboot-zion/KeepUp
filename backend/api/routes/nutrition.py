"""
Nutrition API Routes
Provides personalized meal plans based on workouts and user goals
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from datetime import date, datetime
from typing import Optional

from core.database import get_db
from api.dependencies import get_current_user
from models.user import User
from models.daily_log import UserDailyLog, DailyTask
from agents.adaptive_intervention.nutrition_pivot_agent import NutritionPivotAgent


router = APIRouter(prefix="/nutrition", tags=["Nutrition"])


@router.get("/daily-plan")
async def get_daily_meal_plan(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get personalized meal plan for today based on workout and user state
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
        
        # Get today's workout task
        workout_query = select(DailyTask).where(
            and_(
                DailyTask.user_id == current_user.id,
                DailyTask.date == today,
                DailyTask.task_type == "workout"
            )
        )
        workout_result = await db.execute(workout_query)
        workout_task = workout_result.scalar_one_or_none()
        
        # Prepare context for nutrition agent
        context = {
            "user_id": current_user.id,
            "goal": "weight_loss",  # TODO: Get from user's resolution
            "workout_type": workout_task.description if workout_task else "rest_day",
            "energy_level": checkin.energy_level.value if checkin else "medium",
            "occupation": current_user.occupation or "desk_job",
        }
        
        # Call nutrition agent
        nutrition_agent = NutritionPivotAgent()
        result = await nutrition_agent.analyze(context)
        
        # Format response
        meal_plan = result.get("meal_plan", {})
        
        return {
            "meal_plan": {
                "breakfast": meal_plan.get("breakfast", _default_meal("Breakfast")),
                "lunch": meal_plan.get("lunch", _default_meal("Lunch")),
                "dinner": meal_plan.get("dinner", _default_meal("Dinner")),
                "snacks": meal_plan.get("snacks", []),
                "total_calories": meal_plan.get("total_calories", 2000),
                "total_protein": meal_plan.get("total_protein", 150),
                "total_carbs": meal_plan.get("total_carbs", 200),
                "total_fats": meal_plan.get("total_fats", 60),
            },
            "reasoning": result.get("reasoning", "Personalized meal plan based on your workout"),
            "workout_alignment": result.get("workout_alignment", "This meal plan supports your training goals"),
            "tips": result.get("tips", [
                "Stay hydrated throughout the day",
                "Eat protein within 30 minutes post-workout",
                "Include vegetables with every meal"
            ])
        }
        
    except Exception as e:
        print(f"Error generating meal plan: {e}")
        # Return default meal plan on error
        return {
            "meal_plan": {
                "breakfast": _default_meal("Breakfast"),
                "lunch": _default_meal("Lunch"),
                "dinner": _default_meal("Dinner"),
                "snacks": [],
                "total_calories": 2000,
                "total_protein": 150,
                "total_carbs": 200,
                "total_fats": 60,
            },
            "reasoning": "Default meal plan - complete your daily check-in for personalized recommendations",
            "workout_alignment": "Balanced nutrition for general fitness",
            "tips": [
                "Complete your daily check-in for personalized meal plans",
                "Stay hydrated throughout the day",
                "Eat protein with every meal"
            ]
        }


@router.get("/history")
async def get_nutrition_history(
    days: int = 7,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get nutrition history for the past N days
    """
    # TODO: Store meal plans in database and retrieve history
    return {
        "message": "Nutrition history coming soon",
        "days": days
    }


def _default_meal(meal_type: str) -> dict:
    """Generate a default meal structure"""
    defaults = {
        "Breakfast": {
            "name": "Protein Oatmeal Bowl",
            "description": "Oats with protein powder, berries, and nuts",
            "calories": 450,
            "protein": 30,
            "carbs": 55,
            "fats": 12,
            "ingredients": [
                "1 cup oats",
                "1 scoop protein powder",
                "1/2 cup berries",
                "1 tbsp almond butter"
            ],
            "instructions": [
                "Cook oats with water or milk",
                "Mix in protein powder",
                "Top with berries and almond butter"
            ]
        },
        "Lunch": {
            "name": "Grilled Chicken Salad",
            "description": "Mixed greens with grilled chicken, quinoa, and veggies",
            "calories": 550,
            "protein": 45,
            "carbs": 50,
            "fats": 18,
            "ingredients": [
                "6 oz grilled chicken breast",
                "2 cups mixed greens",
                "1/2 cup quinoa",
                "Assorted vegetables",
                "2 tbsp olive oil dressing"
            ],
            "instructions": [
                "Grill chicken breast",
                "Cook quinoa",
                "Combine all ingredients",
                "Dress with olive oil"
            ]
        },
        "Dinner": {
            "name": "Salmon with Sweet Potato",
            "description": "Baked salmon with roasted sweet potato and broccoli",
            "calories": 650,
            "protein": 50,
            "carbs": 60,
            "fats": 22,
            "ingredients": [
                "6 oz salmon fillet",
                "1 medium sweet potato",
                "2 cups broccoli",
                "1 tbsp olive oil"
            ],
            "instructions": [
                "Bake salmon at 400°F for 15 minutes",
                "Roast sweet potato at 425°F for 30 minutes",
                "Steam broccoli for 5 minutes",
                "Season with herbs and olive oil"
            ]
        }
    }
    return defaults.get(meal_type, defaults["Breakfast"])
