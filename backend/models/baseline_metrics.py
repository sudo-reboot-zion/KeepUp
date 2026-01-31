from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base


class BaselineMetrics(Base):
    """
    Stores the starting health metrics for a resolution.
    These are the baseline values against which progress is measured.
    """
    __tablename__ = "baseline_metrics"

    id = Column(Integer, primary_key=True, index=True)
    resolution_id = Column(Integer, ForeignKey("resolutions.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Cardiovascular metrics
    bp_systolic_baseline = Column(Integer, nullable=True)  # e.g., 140
    bp_diastolic_baseline = Column(Integer, nullable=True)  # e.g., 90
    resting_hr_baseline = Column(Integer, nullable=True)  # beats per minute
    
    # Body composition
    weight_baseline_kg = Column(Float, nullable=True)
    waist_circumference_cm = Column(Float, nullable=True)
    
    # Lifestyle
    avg_sleep_hours_baseline = Column(Float, nullable=True)
    avg_stress_level_baseline = Column(Integer, nullable=True)  # 1-10
    
    # Goals/targets (what user wants to achieve)
    bp_systolic_target = Column(Integer, nullable=True)
    bp_diastolic_target = Column(Integer, nullable=True)
    weight_target_kg = Column(Float, nullable=True)
    resting_hr_target = Column(Integer, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    resolution = relationship("Resolution", back_populates="baseline_metrics")
    goal_progress = relationship("GoalProgress", back_populates="baseline_metrics", cascade="all, delete-orphan")
