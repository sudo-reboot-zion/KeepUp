"""
Biometric API Routes
Handles manual entry and wearable integration for biometric data
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

from core.database import get_db
from api.dependencies import get_current_user
from models.user import User
from agents.biometric_environment.biometric_agent import BiometricAgent
from agents.biometric_environment.environmental_agent import EnvironmentalAgent


router = APIRouter(prefix="/biometric", tags=["Biometric"])


class BiometricEntry(BaseModel):
    heart_rate_resting: Optional[int] = None
    hrv: Optional[int] = None
    weight: Optional[float] = None
    steps: Optional[int] = None
    sleep_hours: Optional[float] = None
    location: Optional[str] = "San Francisco, CA" # Default for now


@router.post("/entry")
async def add_biometric_entry(
    entry: BiometricEntry,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Add manual biometric entry and analyze with environmental context
    """
    # TODO: Save to database
    
    # Analyze with Biometric Agent
    bio_agent = BiometricAgent()
    bio_analysis = await bio_agent.analyze({
        "biometrics": entry.dict(exclude_none=True),
        "user_profile": {"age": 30, "gender": "male"} # Mock profile
    })
    
    # Analyze with Environmental Agent
    env_agent = EnvironmentalAgent()
    env_analysis = await env_agent.analyze({
        "location": entry.location,
        "activity_type": "outdoor_run" # Example context
    })
    
    return {
        "status": "success",
        "biometric_analysis": bio_analysis,
        "environmental_analysis": env_analysis
    }


@router.get("/latest")
async def get_latest_biometrics(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get latest biometric data
    """
    # Mock data
    return {
        "heart_rate_resting": 62,
        "hrv": 45,
        "weight": 185.5,
        "steps": 8432,
        "last_updated": datetime.now()
    }
