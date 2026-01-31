from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base


class NutritionEntry(Base):
    """
    Tracks user's nutrition throughout the day.
    Can be detailed (macros, calories) or simple (quality rating).
    """
    __tablename__ = "nutrition_entry"

    id = Column(Integer, primary_key=True, index=True)
    resolution_id = Column(Integer, ForeignKey("resolutions.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Quick quality rating (simple path for users)
    quality_rating = Column(Integer, nullable=True)  # 1-10 scale
    quality_category = Column(String(50), nullable=True)  # "poor", "fair", "good", "excellent"
    
    # Detailed macros (optional)
    calories = Column(Integer, nullable=True)
    protein_g = Column(Float, nullable=True)
    carbs_g = Column(Float, nullable=True)
    fat_g = Column(Float, nullable=True)
    fiber_g = Column(Float, nullable=True)
    
    # Meal tracking
    meal_type = Column(String(50), nullable=True)  # "breakfast", "lunch", "dinner", "snack"
    
    # What user ate
    foods = Column(Text, nullable=True)  # e.g., "oatmeal, banana, almonds"
    notes = Column(Text, nullable=True)  # user notes about meal
    
    # Adherence flags
    on_track = Column(String(50), nullable=True)  # "yes", "no", "partial"
    
    # Metadata
    date = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    resolution = relationship("Resolution", back_populates="nutrition_entries")
    user = relationship("User")
