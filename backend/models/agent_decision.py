from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base


class AgentDecision(Base):
    """
    Full decision log for agent reasoning chains.
    Every agent decision is logged here for Opik traceability and analysis.
    Shows what input was processed, how agent reasoned, what output was produced.
    """
    __tablename__ = "agent_decision"

    id = Column(Integer, primary_key=True, index=True)
    resolution_id = Column(Integer, ForeignKey("resolutions.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Decision metadata
    decision_type = Column(String(100), nullable=False)  # "adapt_workout", "nutrition_advice", "recovery_needed", etc
    agent_name = Column(String(100), nullable=False)  # Which agent made this?
    
    # Input context
    input_context = Column(JSON, nullable=False)  # Full context passed to agent (sleep, stress, etc)
    
    # Reasoning chain
    reasoning_chain = Column(Text, nullable=False)  # LLM thinking/reasoning
    reasoning_steps = Column(JSON, nullable=True)  # Structured steps of reasoning
    
    # Output
    decision_output = Column(Text, nullable=False)  # What agent decided
    
    # Confidence and metrics
    confidence_score = Column(Float, nullable=False)  # 0.0-1.0
    decision_certainty = Column(String(50), nullable=True)  # "high", "medium", "low"
    
    # Safety checks
    safety_check_passed = Column(String(50), default="yes")  # "yes", "warning", "blocked"
    safety_warnings = Column(Text, nullable=True)
    
    # Opik integration
    opik_trace_id = Column(String(255), nullable=True)  # Full Opik trace URL
    opik_experiment_name = Column(String(255), nullable=True)
    opik_run_name = Column(String(255), nullable=True)
    
    # Outcome
    user_feedback = Column(Text, nullable=True)
    outcome_success = Column(String(50), nullable=True)  # "success", "partial", "failure"
    
    # Additional context
    tags = Column(JSON, nullable=True)  # ["high_stress", "low_sleep", "adaptation_needed"]
    decision_metadata = Column(JSON, nullable=True)  # Additional agent-specific data
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    resolution = relationship("Resolution", back_populates="agent_decisions")
