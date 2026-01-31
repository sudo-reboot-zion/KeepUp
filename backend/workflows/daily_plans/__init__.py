"""
Daily Plan Generators
Goal-specific daily plan generators for personalized health workflows
"""
from workflows.daily_plans.base_plan_generator import BaseDailyPlanGenerator
from workflows.daily_plans.fitness_daily_plan import fitness_daily_plan_generator
from workflows.daily_plans.sleep_daily_plan import sleep_daily_plan_generator
from workflows.daily_plans.stress_daily_plan import stress_daily_plan_generator
from workflows.daily_plans.wellness_daily_plan import wellness_daily_plan_generator


def get_plan_generator(primary_goal: str) -> BaseDailyPlanGenerator:
    """
    Factory function to get the appropriate plan generator based on primary goal.
    
    Args:
        primary_goal: User's primary health goal ("fitness"|"sleep"|"stress"|"wellness")
    
    Returns:
        Appropriate daily plan generator instance
    """
    generators = {
        "fitness": fitness_daily_plan_generator,
        "sleep": sleep_daily_plan_generator,
        "stress": stress_daily_plan_generator,
        "wellness": wellness_daily_plan_generator
    }
    
    generator = generators.get(primary_goal)
    if not generator:
        # Default to wellness if unknown goal
        return wellness_daily_plan_generator
    
    return generator


__all__ = [
    "BaseDailyPlanGenerator",
    "fitness_daily_plan_generator",
    "sleep_daily_plan_generator",
    "stress_daily_plan_generator",
    "wellness_daily_plan_generator",
    "get_plan_generator"
]
