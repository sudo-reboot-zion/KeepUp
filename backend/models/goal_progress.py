from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base


class GoalProgress(Base):
    """
    Tracks progress toward a specific health goal metric.
    Links baseline metrics to current readings and shows trend.
    Used for displaying goal achievement and causality analysis.
    """
    __tablename__ = "goal_progress"

    id = Column(Integer, primary_key=True, index=True)
    resolution_id = Column(Integer, ForeignKey("resolutions.id", ondelete="CASCADE"), nullable=False, index=True)
    baseline_metrics_id = Column(Integer, ForeignKey("baseline_metrics.id", ondelete="CASCADE"), nullable=False)
    
    # Which metric are we tracking?
    metric_type = Column(String(100), nullable=False)  # "blood_pressure", "weight", "resting_hr", "waist_circumference"
    metric_unit = Column(String(50), nullable=False)  # "mmHg", "kg", "bpm", "cm"
    
    # Baseline and target
    baseline_value = Column(Float, nullable=False)  # Starting point
    target_value = Column(Float, nullable=False)  # Goal/endpoint
    
    # Current state
    current_value = Column(Float, nullable=True)  # Latest measurement
    days_elapsed = Column(Integer, nullable=False)  # Days since resolution start
    
    # Progress tracking
    value_change = Column(Float, nullable=True)  # current - baseline (can be negative)
    percentage_progress = Column(Float, nullable=True)  # (change / (target - baseline)) * 100
    
    # Trend analysis
    trend_direction = Column(String(50), nullable=True)  # "improving", "stable", "declining"
    trend_strength = Column(String(50), nullable=True)  # "strong", "moderate", "weak", "no_data"
    days_to_goal_estimate = Column(Integer, nullable=True)  # Projection
    
    # Contributing factors (causality)
    contributing_factors = Column(Text, nullable=True)  # JSON of factors contributing to progress
    # Example: {"workouts_completed": 18, "avg_sleep_hours": 7.2, "nutrition_quality": "good"}
    
    # Insight for user
    insight_text = Column(Text, nullable=True)  # Human-readable insight about progress
    # Example: "Your 1.5h sleep improvement + 3 workouts per week = 8-point BP reduction"
    
    # Last measurement
    last_measurement_date = Column(DateTime, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    resolution = relationship("Resolution", back_populates="goal_progress")
    baseline_metrics = relationship("BaselineMetrics", back_populates="goal_progress")
