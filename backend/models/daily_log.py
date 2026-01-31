from datetime import date, datetime
from typing import Optional
from sqlalchemy import String, Integer, Boolean, Date, DateTime, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
import enum

from models.user import Base

class EnergyLevel(str, enum.Enum):
    ENERGIZED = "energized"
    NORMAL = "normal"
    TIRED = "tired"
    EXHAUSTED = "exhausted"

class SorenessLevel(str, enum.Enum):
    NONE = "none"
    MILD = "mild"
    MODERATE = "moderate"
    SIGNIFICANT = "significant"

class StressLevel(str, enum.Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    OVERWHELMING = "overwhelming"

class TaskType(str, enum.Enum):
    WORKOUT = "workout"
    NUTRITION = "nutrition"
    HYDRATION = "hydration"
    RECOVERY = "recovery"
    MINDFULNESS = "mindfulness"
    WORK = "work"
    CUSTOM = "custom"

class TaskSource(str, enum.Enum):
    AI = "ai"
    USER = "user"

class UserDailyLog(Base):
    __tablename__ = "daily_checkins"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    
    # User reported state
    sleep_quality: Mapped[int] = mapped_column(Integer, nullable=False) # 1-5
    energy_level: Mapped[EnergyLevel] = mapped_column(SQLEnum(EnergyLevel), nullable=False)
    soreness_level: Mapped[SorenessLevel] = mapped_column(SQLEnum(SorenessLevel), nullable=False)
    stress_level: Mapped[StressLevel] = mapped_column(SQLEnum(StressLevel), nullable=False)
    
    # Mental Health & Reflection
    mood_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True) # 1-10
    anxiety_level: Mapped[Optional[int]] = mapped_column(Integer, nullable=True) # 1-10
    gratitude_log: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    wins_log: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    challenges_log: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False
    )

    # Relationships
    user = relationship("User", backref="checkins")

class DailyTask(Base):
    __tablename__ = "daily_tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    task_type: Mapped[TaskType] = mapped_column(SQLEnum(TaskType), default=TaskType.CUSTOM, nullable=False)
    
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    source: Mapped[TaskSource] = mapped_column(SQLEnum(TaskSource), default=TaskSource.USER, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False
    )

    # Relationships
    user = relationship("User", backref="tasks")
