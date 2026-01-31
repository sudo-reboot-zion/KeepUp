"""
Resolution Model
Represents a user's fitness resolution/goal with AI-generated plan
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from models.user import Base
import enum


class ResolutionStatus(str, enum.Enum):
    """Resolution lifecycle states"""
    ACTIVE = "active"
    COMPLETED = "completed"
    ABANDONED = "abandoned"
    PAUSED = "paused"


class Resolution(Base):
    """
    User's fitness resolution with AI-generated plan
    Created via OnboardingWorkflow
    """
    __tablename__ = "resolutions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Original user input
    resolution_text = Column(Text, nullable=False)  # "I want to lose 20 lbs"
    past_attempts = Column(Text, nullable=True)  # User's history
    life_constraints = Column(JSON, nullable=True)  # ["busy_schedule", "travel_frequently"]
    
    # Primary Health Goal (MVP Core Feature)
    primary_goal = Column(
        String(50), 
        nullable=True,
        comment="User's primary health focus: fitness|sleep|stress|wellness"
    )
    supporting_goals = Column(
        JSON, 
        nullable=True,
        comment="Secondary goals that support primary goal"
    )
    goal_focus_percentage = Column(
        JSON,
        nullable=True,
        comment="How focus is split: {primary: 70, supporting: 30}"
    )
    
    # AI-generated plan (from OnboardingWorkflow)
    final_plan = Column(JSON, nullable=False)  # Complete workout plan
    debate_summary = Column(JSON, nullable=True)  # Agent debate results
    confidence_score = Column(Float, nullable=True)  # AI confidence in plan
    
    # Status tracking
    status = Column(SQLEnum(ResolutionStatus), default=ResolutionStatus.ACTIVE, nullable=False, index=True)
    current_week = Column(Integer, default=1, nullable=False)
    
    # Progress metrics
    workouts_completed = Column(Integer, default=0, nullable=False)
    workouts_target = Column(Integer, nullable=True)  # Weekly target
    adherence_rate = Column(Float, default=0.0, nullable=False)  # 0.0 to 1.0
    streak_days = Column(Integer, default=0, nullable=False)
    
    # Risk tracking
    abandonment_probability = Column(Float, default=0.0, nullable=False)  # AI prediction
    last_intervention_at = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    abandoned_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", backref="resolutions")
    baseline_metrics = relationship("BaselineMetrics", back_populates="resolution", cascade="all, delete-orphan", uselist=False)
    daily_checkins = relationship("DailyCheckIn", back_populates="resolution", cascade="all, delete-orphan")
    biometric_readings = relationship("BiometricReading", back_populates="resolution", cascade="all, delete-orphan")
    weekly_biometrics = relationship("WeeklyBiometrics", back_populates="resolution", cascade="all, delete-orphan")
    nutrition_entries = relationship("NutritionEntry", back_populates="resolution", cascade="all, delete-orphan")
    agent_recommendations = relationship("AgentRecommendation", back_populates="resolution", cascade="all, delete-orphan")
    agent_decisions = relationship("AgentDecision", back_populates="resolution", cascade="all, delete-orphan")
    goal_progress = relationship("GoalProgress", back_populates="resolution", cascade="all, delete-orphan")
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "resolution_text": self.resolution_text,
            "status": self.status.value,
            "current_week": self.current_week,
            "workouts_completed": self.workouts_completed,
            "adherence_rate": self.adherence_rate,
            "streak_days": self.streak_days,
            "abandonment_probability": self.abandonment_probability,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    def get_plan_summary(self):
        """Get human-readable plan summary"""
        if not self.final_plan:
            return None
        
        return {
            "goal": self.final_plan.get("interpreted_goal"),
            "weekly_target": self.final_plan.get("weekly_target"),
            "first_milestone": self.final_plan.get("first_milestone"),
            "confidence": self.confidence_score
        }
