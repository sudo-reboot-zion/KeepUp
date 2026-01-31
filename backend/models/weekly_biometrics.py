from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Table, String
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base


# Association table for many-to-many relationship
weekly_biometrics_readings = Table(
    'weekly_biometrics_readings',
    Base.metadata,
    Column('weekly_biometrics_id', Integer, ForeignKey('weekly_biometrics.id', ondelete='CASCADE')),
    Column('biometric_reading_id', Integer, ForeignKey('biometric_reading.id', ondelete='CASCADE'))
)


class WeeklyBiometrics(Base):
    """
    Aggregated biometric measurements for a week.
    Used to smooth out daily fluctuations and see true trends.
    Calculated from all BiometricReadings in that week.
    """
    __tablename__ = "weekly_biometrics"

    id = Column(Integer, primary_key=True, index=True)
    resolution_id = Column(Integer, ForeignKey("resolutions.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Week identifier
    week_number = Column(Integer, nullable=False)  # 1-52
    year = Column(Integer, nullable=False)
    
    # Average/aggregated blood pressure
    avg_bp_systolic = Column(Integer, nullable=True)
    avg_bp_diastolic = Column(Integer, nullable=True)
    min_bp_systolic = Column(Integer, nullable=True)
    max_bp_systolic = Column(Integer, nullable=True)
    
    # Average heart rate
    avg_resting_hr = Column(Integer, nullable=True)
    
    # Average weight
    avg_weight_kg = Column(Float, nullable=True)
    weight_change_from_baseline = Column(Float, nullable=True)  # kg delta
    
    # Average waist circumference
    avg_waist_circumference_cm = Column(Float, nullable=True)
    
    # Sample counts (how many readings this week?)
    bp_reading_count = Column(Integer, default=0)
    weight_reading_count = Column(Integer, default=0)
    
    # Trend analysis
    trend_direction = Column(String(50), nullable=True)  # "improving", "stable", "declining"
    trend_strength = Column(String(50), nullable=True)  # "strong", "moderate", "weak"
    
    # Metadata
    week_start_date = Column(DateTime, nullable=False)
    week_end_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    resolution = relationship("Resolution", back_populates="weekly_biometrics")
    biometric_readings = relationship("BiometricReading", secondary=weekly_biometrics_readings, back_populates="weekly_biometrics")
