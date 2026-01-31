"""Alert acknowledgment tracking model"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship

from core.database import Base


class AlertAcknowledgment(Base):
    """
    Tracks when users acknowledge critical safety alerts.
    Used for medical compliance and follow-up.
    """
    __tablename__ = "alert_acknowledgments"
    
    id = Column(Integer, primary_key=True, index=True)
    resolution_id = Column(Integer, ForeignKey("resolutions.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Alert details
    alert_type = Column(String(50), nullable=False)  # "critical", "warning", "blocked"
    alert_category = Column(String(50), nullable=False)  # "medical", "confidence", "overtraining"
    alert_message = Column(String(500), nullable=False)
    alert_metric = Column(String(100), nullable=True)  # e.g., "bp_systolic"
    
    # Alert readings
    metric_value = Column(String(100), nullable=True)  # e.g., "185"
    threshold_value = Column(String(100), nullable=True)  # e.g., "180"
    
    # Acknowledgment
    acknowledged_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    user_notes = Column(String(500), nullable=True)
    
    # Follow-up
    action_taken = Column(String(255), nullable=True)
    action_confirmed_at = Column(DateTime, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    resolution = relationship("Resolution")
    user = relationship("User")
    
    def __repr__(self):
        return f"<AlertAcknowledgment(user={self.user_id}, type={self.alert_type}, metric={self.alert_metric})>"
