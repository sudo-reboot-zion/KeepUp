from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class NotificationBase(BaseModel):
    title: str
    message: str
    type: str  # intervention, progress, reminder, achievement
    category: str  # ai_coach, system, social
    data: Optional[Dict[str, Any]] = None
    priority: str = "normal"


class NotificationResponse(NotificationBase):
    id: int
    user_id: int
    read: bool
    read_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationListResponse(BaseModel):
    notifications: List[NotificationResponse]
    unread_count: int


class NotificationCountResponse(BaseModel):
    count: int


class MarkReadResponse(BaseModel):
    success: bool
    count: Optional[int] = None
