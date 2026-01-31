"""
QuarterlyPhase Model
Represents a quarter (13 weeks) within a yearly resolution
Q1: Foundation | Q2: Progression | Q3: Mastery | Q4: Acceleration
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, ForeignKey, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship
from models.user import Base
import enum


class QuarterNumber(str, enum.Enum):
    """Quarter identifier"""
    Q1 = "Q1"
    Q2 = "Q2"
    Q3 = "Q3"
    Q4 = "Q4"


class QuarterlyPhase(Base):
    """
    Quarter-level breakdown of a yearly resolution
    
    Example:
    - Resolution: "Run 5K by Dec 31, 2026"
    - Q1: Foundation (Weeks 1-13) - Build habit, prove consistency
    - Q2: Progression (Weeks 14-26) - Increase difficulty, add variety
    - Q3: Mastery (Weeks 27-39) - Build endurance, manage plateaus
    - Q4: Acceleration (Weeks 40-52) - Final push, goal attempt
    """
    __tablename__ = "quarterly_phases"
    
    id = Column(Integer, primary_key=True, index=True)
    resolution_id = Column(Integer, ForeignKey("resolutions.id"), nullable=False, index=True)
    
    # Quarter identifier
    quarter = Column(SQLEnum(QuarterNumber), nullable=False)  # Q1, Q2, Q3, Q4
    week_start = Column(Integer, nullable=False)  # Week 1, 14, 27, 40
    week_end = Column(Integer, nullable=False)    # Week 13, 26, 39, 52
    
    # Phase info
    phase_name = Column(String(50), nullable=False)  # "Foundation", "Progression", "Mastery", "Acceleration"
    phase_description = Column(Text, nullable=False)  # "Build habit, prove consistency"
    focus_areas = Column(JSON, nullable=False)  # ["habit_formation", "consistency", "routine_building"]
    
    # Targets for the quarter
    target_workouts = Column(Integer, nullable=False)  # Total workouts in quarter (e.g., 39 for Q1: 3/week * 13 weeks)
    target_metric = Column(Text, nullable=True)  # "Distance: 3 miles per session"
    target_progression = Column(Text, nullable=True)  # "Increase from 20min to 25min sessions"
    
    # Milestones within quarter (checkpoints)
    milestones = Column(JSON, nullable=False)  # [{"week": 4, "goal": "Pass week 3 cliff"}, ...]
    
    # Progress tracking
    workouts_completed = Column(Integer, default=0, nullable=False)
    adherence_rate = Column(Float, default=0.0, nullable=False)  # 0.0 to 1.0
    
    # Risks to watch (from Failure Pattern Agent)
    risk_factors = Column(JSON, nullable=False)  # ["motivation_cliff", "plateau_zone", "life_event_collision"]
    protective_strategies = Column(JSON, nullable=False)  # ["extra_accountability", "variation_in_workouts"]
    
    # Status
    status = Column(String(20), default="locked", nullable=False)  # "completed", "in_progress", "locked"
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    resolution = relationship("Resolution", backref="quarterly_phases")
    weekly_plans = relationship("WeeklyPlan", back_populates="quarterly_phase", cascade="all, delete-orphan")
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "resolution_id": self.resolution_id,
            "quarter": self.quarter.value,
            "week_start": self.week_start,
            "week_end": self.week_end,
            "phase_name": self.phase_name,
            "phase_description": self.phase_description,
            "focus_areas": self.focus_areas,
            "target_workouts": self.target_workouts,
            "target_metric": self.target_metric,
            "workouts_completed": self.workouts_completed,
            "adherence_rate": self.adherence_rate,
            "milestones": self.milestones,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    @property
    def completion_percentage(self) -> float:
        """Calculate quarter completion percentage"""
        if self.target_workouts == 0:
            return 0.0
        return (self.workouts_completed / self.target_workouts) * 100
