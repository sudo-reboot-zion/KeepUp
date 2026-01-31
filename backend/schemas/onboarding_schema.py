from pydantic import BaseModel
from typing import Optional, List

class OnboardingRequest(BaseModel):
    # Primary Health Goal (MVP Core Feature)
    primary_goal: str  # "fitness"|"sleep"|"stress"|"wellness"
    goal_details: str  # Specific details about their goal
    
    # Legacy/Supporting fields
    resolution_text: Optional[str] = None  # Deprecated in favor of goal_details
    past_attempts: Optional[str] = None
    life_constraints: Optional[List[str]] = None
    occupation: Optional[str] = None
    occupation_details: Optional[dict] = None


class OnboardingResponse(BaseModel):
    final_plan: dict
    debate_summary: dict
    confidence_score: float
