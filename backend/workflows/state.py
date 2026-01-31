"""
Shared state definitions for LangGraph workflows.
All agents read and write to these state objects.
"""
from typing import TypedDict, Optional, List, Dict, Any
from datetime import datetime


class OnboardingState(TypedDict):
    """
    State for the onboarding workflow.
    Passed between Goal Setting Agent → Failure Pattern Agent → Meta-Coordinator
    """
    # User inputs
    user_id: str
    resolution_text: str 
    past_attempts: Optional[str]
    life_constraints: Optional[List[str]] 
    occupation: Optional[str]
    occupation_details: Optional[Dict[str, Any]] 
    
    goal_analysis: Optional[Dict[str, Any]]  
    failure_risk: Optional[Dict[str, Any]]  
    
    # Final outputs
    final_plan: Optional[Dict[str, Any]]  
    debate_summary: Optional[Dict[str, Any]]
    safety_adjustments: Optional[List[str]]
    confidence_score: Optional[float]  
    
    # Memory management (LangGraph-compatible)
    user_memory: Optional[Dict[str, Any]]  # Loaded memories from database
    memory_updates: Optional[List[Dict[str, Any]]]  # New learnings to persist
    
    # Metadata
    timestamp: Optional[str]
    errors: Optional[List[str]] 
    _user_profile: Optional[Dict[str, Any]]


class DailyCheckState(TypedDict):
    """
    State for daily check workflow.
    Used by multiple agents to generate today's adaptive plan.
    """
    # User context
    user_id: str
    current_date: str

    sleep_data: Optional[Dict[str, Any]] 
    calendar_events: Optional[List[Dict]]  
    recent_workouts: Optional[List[Dict]] 
    stress_score: Optional[float] 
    
    # Agent analyses
    biometric_analysis: Optional[Dict[str, Any]]
    occupation_analysis: Optional[Dict[str, Any]]
    schedule_conflicts: Optional[List[str]]
    motivation_level: Optional[str]
    
    # Recommendations
    workout_plan: Optional[Dict[str, Any]]
    adaptations: Optional[List[str]] 
    
    # Final output
    daily_plan: Optional[Dict[str, Any]]
    confidence_score: Optional[float]
    
    # Memory management (LangGraph-compatible)
    user_memory: Optional[Dict[str, Any]]  # Loaded memories from database
    memory_updates: Optional[List[Dict[str, Any]]]  # New learnings to persist
    
    # Metadata
    timestamp: Optional[str]
    errors: Optional[List[str]]


class InterventionState(TypedDict):
    """
    State for intervention workflow.
    Used when user is at risk of abandoning resolution.
    """
    # User context
    user_id: str
    
    missed_workouts: int
    days_inactive: int
    current_week: int
    historical_quit_week: Optional[int]
    
    abandonment_probability: Optional[float]  
    detected_barriers: Optional[List[str]]
    motivation_drop: Optional[bool]
    
    intervention_type: Optional[str] 
    recommended_actions: Optional[List[Dict]]
    alternative_plans: Optional[List[Dict]]
    
    intervention_plan: Optional[Dict[str, Any]]
    confidence_score: Optional[float]
    
    # Memory management (LangGraph-compatible)
    user_memory: Optional[Dict[str, Any]]  # Loaded memories from database
    memory_updates: Optional[List[Dict[str, Any]]]  # New learnings to persist
    
    # Metadata
    timestamp: Optional[str]
    errors: Optional[List[str]]
