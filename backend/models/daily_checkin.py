from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base


class DailyCheckIn(Base):
    """
    Daily health check-in capturing subjective user inputs.
    Tracks sleep, stress, mood, energy, and symptom data.
    """
    __tablename__ = "daily_checkin"

    id = Column(Integer, primary_key=True, index=True)
    resolution_id = Column(Integer, ForeignKey("resolutions.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Sleep data
    sleep_hours = Column(Float, nullable=True)  # e.g., 7.5
    sleep_quality = Column(Integer, nullable=True)  # 1-10 rating
    
    # Stress & mood
    stress_level = Column(Integer, nullable=True)  # 1-10 scale
    mood = Column(String(50), nullable=True)  # e.g., "energetic", "tired", "anxious"
    energy_level = Column(Integer, nullable=True)  # 1-10 scale
    
    # Symptoms & notes
    symptoms = Column(Text, nullable=True)  # e.g., "headache", "sore muscles", "joint pain"
    notes = Column(Text, nullable=True)  # free-form user notes
    
    # Workout readiness (subjective)
    ready_for_workout = Column(String(50), nullable=True)  # "yes", "partial", "no"
    
    # Metadata
    date = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    resolution = relationship("Resolution", back_populates="daily_checkins")
    user = relationship("User")
    agent_recommendations = relationship("AgentRecommendation", back_populates="daily_checkin")
