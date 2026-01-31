from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base


class BiometricReading(Base):
    """
    Objective biometric measurements taken by user.
    Can be daily or weekly depending on user preference.
    Used to track goal progress (BP reduction, weight loss, etc).
    """
    __tablename__ = "biometric_reading"

    id = Column(Integer, primary_key=True, index=True)
    resolution_id = Column(Integer, ForeignKey("resolutions.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Blood pressure (mmHg)
    bp_systolic = Column(Integer, nullable=True)  # e.g., 135
    bp_diastolic = Column(Integer, nullable=True)  # e.g., 85
    
    # Heart rate (bpm)
    resting_hr = Column(Integer, nullable=True)
    
    # Body composition
    weight_kg = Column(Float, nullable=True)
    waist_circumference_cm = Column(Float, nullable=True)
    
    # Body composition (optional advanced)
    body_fat_percentage = Column(Float, nullable=True)
    
    # Timing of measurement
    time_of_day = Column(String(50), nullable=True)  # "morning", "afternoon", "evening"
    
    # Context (helps interpret readings)
    context_notes = Column(String(255), nullable=True)  # e.g., "measured after coffee", "after workout"
    
    # Data source
    source = Column(String(100), nullable=True)  # "manual", "apple_watch", "fitbit", "smart_scale"
    
    # Metadata
    date = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    resolution = relationship("Resolution", back_populates="biometric_readings")
    user = relationship("User")
    weekly_biometrics = relationship("WeeklyBiometrics", back_populates="biometric_readings", secondary="weekly_biometrics_readings")
