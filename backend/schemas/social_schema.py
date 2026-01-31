"""
Pydantic schemas for social community features
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class PartnershipCreate(BaseModel):
    partner_user_id: int


class PartnershipResponse(BaseModel):
    id: int
    user_id_1: int
    user_id_2: int
    status: str
    match_reason: Optional[str] = None
    matched_on: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class PartnerSuggestion(BaseModel):
    user_id: int
    display_name: str
    occupation: Optional[str] = None
    goal: Optional[str] = None
    match_score: float


class GroupCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    max_members: int = Field(default=10, ge=5, le=20)


class GroupResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    max_members: int
    created_by: int
    created_at: datetime
    member_count: int = 0
    
    class Config:
        from_attributes = True


class MessageCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=500)
    message_type: str = Field(default="text")


class MessageResponse(BaseModel):
    id: int
    group_id: int
    user_id: int
    user_display_name: str
    message_type: str
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class EncouragementCreate(BaseModel):
    to_user_id: int
    template_id: Optional[str] = None
    custom_message: Optional[str] = Field(None, max_length=200)


class MilestoneResponse(BaseModel):
    id: int
    user_id: int
    milestone_type: str
    achieved_at: datetime
    is_celebrated: bool
    
    class Config:
        from_attributes = True
