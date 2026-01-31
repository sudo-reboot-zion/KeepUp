"""
Base Daily Plan Generator
Abstract base class for goal-specific daily plan generators
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from datetime import datetime


class BaseDailyPlanGenerator(ABC):
    """
    Abstract base class for generating personalized daily plans.
    
    Each goal type (fitness, sleep, stress, wellness) has its own generator
    that inherits from this base class.
    """
    
    def __init__(self, goal_type: str):
        self.goal_type = goal_type
    
    @abstractmethod
    async def generate(
        self,
        user_profile: Dict[str, Any],
        biometrics: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate personalized daily plan.
        
        Args:
            user_profile: User's profile including primary_goal, occupation, etc.
            biometrics: Today's biometric data (sleep, energy, stress, soreness)
            context: Additional context (interventions, barriers, schedule)
        
        Returns:
            {
                "goal_type": "fitness|sleep|stress|wellness",
                "primary_focus": {...},  # 70% of daily plan
                "supporting_activities": {...},  # 30% of daily plan
                "morning_briefing": str,
                "tasks": List[Dict],
                "interventions": List[Dict],
                "success_metrics": Dict
            }
        """
        pass
    
    def _calculate_focus_split(self, primary_weight: float = 0.7) -> Dict[str, float]:
        """
        Calculate how to split focus between primary and supporting goals.
        Default: 70% primary, 30% supporting
        """
        return {
            "primary": primary_weight,
            "supporting": 1.0 - primary_weight
        }
    
    def _prioritize_interventions(
        self,
        interventions: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Prioritize interventions based on goal type.
        
        Example: Fitness user with poor sleep
        - Sleep intervention is supporting (lower priority)
        
        Sleep user with poor sleep
        - Sleep intervention is primary (highest priority)
        """
        if not interventions:
            return []
        
        # Sort by severity and relevance to goal
        prioritized = sorted(
            interventions,
            key=lambda x: (
                self._get_intervention_priority(x["type"]),
                x.get("severity", "medium")
            ),
            reverse=True
        )
        
        return prioritized
    
    @abstractmethod
    def _get_intervention_priority(self, intervention_type: str) -> int:
        """
        Return priority score for intervention type based on goal.
        Higher score = higher priority
        """
        pass
    
    def _build_morning_briefing(
        self,
        user_name: str,
        primary_focus: Dict[str, Any],
        supporting_activities: Dict[str, Any],
        biometrics: Dict[str, Any]
    ) -> str:
        """
        Build personalized morning briefing message.
        Overridden by each goal-specific generator.
        """
        return f"Good morning, {user_name}!"
    
    def _generate_tasks(
        self,
        primary_focus: Dict[str, Any],
        supporting_activities: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Generate actionable tasks for the day.
        Overridden by each goal-specific generator.
        """
        return []
    
    def _calculate_success_metrics(
        self,
        plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Define what success looks like for this day.
        """
        return {
            "primary_goal_completion": 0.0,
            "supporting_activities_completion": 0.0,
            "overall_adherence": 0.0
        }
