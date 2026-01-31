from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict



# schemas/user_schema.py

class UserBase(BaseModel):
    """Base user schema with common fields"""
    username: str = Field(..., min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_\s]+$")
    email: EmailStr
    display_name: str = Field(..., min_length=1, max_length=100)
    bio: Optional[str] = Field(None, max_length=500)
    
    age: Optional[int] = Field(None, ge=13, le=120)  # Must be 13+
    gender: Optional[str] = Field(None, pattern=r"^(male|female|non-binary|prefer_not_to_say)$")
    tracks_menstrual_cycle: bool = False


class UserCreate(BaseModel):
    """Schema for user registration"""
    username: str = Field(..., min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_\s]+$")
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    display_name: str = Field(..., min_length=1, max_length=100)
    bio: Optional[str] = Field(None, max_length=500)
    
    age: Optional[int] = Field(None, ge=13, le=120)
    gender: Optional[str] = None
    tracks_menstrual_cycle: bool = False


class UserResponse(BaseModel):
    """User data returned to client"""
    id: int
    username: str
    email: str
    display_name: str
    bio: Optional[str] = None
    has_completed_onboarding: bool = False
    
    # Primary Health Goal
    primary_goal: Optional[str] = None
    goal_details: Optional[dict] = None
    goal_set_at: Optional[datetime] = None
    
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserHealthUpdate(BaseModel):
    """Schema for updating health tracking info"""
    cycle_day: Optional[int] = Field(None, ge=1, le=28)
    last_period_date: Optional[datetime] = None
    tracks_menstrual_cycle: Optional[bool] = None


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str



class UserProfile(UserResponse):
    """Extended user profile with additional info"""
    # UserResponse already has: id, username, display_name, bio, age, gender, created_at
    
    # Add any extra fields for profile view
    post_count: int = 0
    workout_count: int = 0
    current_streak: int = 0
    
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str = "bearer"



class TokenData(BaseModel):
    """Schema for token payload data"""
    user_id: Optional[int] = None
    username: Optional[str] = None


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
    detail: Optional[str] = None


