"""
Challenge Model
Represents a community challenge that users can join.
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Text, ForeignKey, DateTime, Boolean, Integer, JSON, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from core.database import Base

class Challenge(Base):
    __tablename__ = "challenges"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # Challenge Details
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)  # fitness, sleep, stress, wellness
    difficulty: Mapped[str] = mapped_column(String(20), default="beginner")
    
    # Timing
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    duration_days: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Participation Stats (Updated by Community Agent)
    participants_count: Mapped[int] = mapped_column(Integer, default=0)
    completion_rate: Mapped[float] = mapped_column(Float, default=0.0)
    
    # AI Generation Metadata
    generated_by_agent: Mapped[str] = mapped_column(String(50), default="Community Agent")
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    participants = relationship("UserChallenge", back_populates="challenge")


class UserChallenge(Base):
    """Link table for users joining challenges"""
    __tablename__ = "user_challenges"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    challenge_id: Mapped[int] = mapped_column(ForeignKey("challenges.id"), nullable=False)
    
    # Progress
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    days_completed: Mapped[int] = mapped_column(Integer, default=0)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String(20), default="active")  # active, completed, dropped
    
    challenge = relationship("Challenge", back_populates="participants")
    user = relationship("User", backref="challenges")
