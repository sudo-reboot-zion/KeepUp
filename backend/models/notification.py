# models/notification.py

"""
Notification Model - In-app notifications stored in database
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base


class Notification(Base):
    """
    In-app notifications for users.
    Stored in database and optionally sent via WebSocket.
    """
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Notification content
    type = Column(String, nullable=False)  # intervention, progress, reminder, achievement
    category = Column(String, nullable=False)  # ai_coach, system, social
    title = Column(String, nullable=False)
    message = Column(String, nullable=False)
    data = Column(JSON, nullable=True)  # Additional structured data
    
    # Metadata
    priority = Column(String, default="normal")  # low, normal, high
    read = Column(Boolean, default=False, index=True)
    read_at = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    user = relationship("User", back_populates="notifications")
