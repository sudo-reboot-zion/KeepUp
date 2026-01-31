from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Text, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, Text
from core.database import Base


# models/user.py

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    age: Mapped[Optional[int]] = mapped_column(nullable=True)
    gender: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # male, female, non-binary, prefer_not_to_say
    

    has_completed_onboarding: Mapped[bool] = mapped_column(default=False, nullable=False)
    
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    tracks_menstrual_cycle: Mapped[bool] = mapped_column(default=False, nullable=False)
    cycle_day: Mapped[Optional[int]] = mapped_column(nullable=True)  # 1-28
    last_period_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


    occupation: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    occupation_details: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    

    primary_goal: Mapped[Optional[str]] = mapped_column(
        String(50), 
        nullable=True,
        comment="User's primary health focus: fitness|sleep|stress|wellness"
    )
    goal_details: Mapped[Optional[dict]] = mapped_column(
        JSON, 
        nullable=True,
        comment="Rich context about user's specific goal"
    )
    
    # Notification Preferences (US 5.1)
    notification_preferences: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
        default={
            "morning_briefing": {"enabled": True, "time": "07:00"},
            "evening_wind_down": {"enabled": True, "time": "21:00"},
            "workout_reminders": {"enabled": True, "time": "variable"},
            "milestones": {"enabled": True, "mute": False},
            "quiet_hours": {"start": "22:00", "end": "06:00"},
            "channels": {"push": True, "email": False, "sms": False},
            "paused_until": None  # ISO datetime string
        },
        comment="User settings for notification timing, channels, and quiet hours"
    )
    goal_set_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), 
        nullable=True,
        comment="When user set their primary goal"
    )
   
    memories = relationship("UserMemory", back_populates="user")
    workout_sessions = relationship("WorkoutSession", back_populates="user", cascade="all, delete-orphan")
    life_events = relationship("LifeEvent", back_populates="user", cascade="all, delete-orphan")


    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )






class UserMemory(Base):
    """
    Stores what agents learn about users over time
    """
    __tablename__ = "user_memories"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # What learned
    agent_name = Column(String(100), nullable=False, index=True)
    learning_type = Column(String(50), nullable=False, index=True)
    content = Column(JSON, nullable=False)
    
    # Confidence and lifecycle
    confidence = Column(Float, default=1.0)  # 0.0 to 1.0
    expires_at = Column(DateTime, nullable=True)  # Auto-delete after this date
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="memories")
