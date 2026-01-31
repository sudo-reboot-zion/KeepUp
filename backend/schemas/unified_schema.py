from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class ChatMessageRequest(BaseModel):
    """Send message to AI coach (non-WebSocket fallback)"""
    message: str
    context: Dict[str, Any] = {}


class ChatMessageResponse(BaseModel):
    """AI coach response"""
    message: str
    data: Dict[str, Any] = {}
    actions: List[str] = []
    confidence: float
    timestamp: str
