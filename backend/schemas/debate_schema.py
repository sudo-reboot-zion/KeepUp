# schemas/debate_schema.py

"""
Debate Schemas - For multi-agent debate system
Transparent AI decision-making through agent debates
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


# ============================================================================
# AGENT POSITION SCHEMAS
# ============================================================================

class AgentPositionResponse(BaseModel):
    """Single agent's position in a debate"""
    agent_name: str
    stance: str  # "support", "challenge", "conditional"
    reasoning: str
    concerns: List[str] = []
    counter_proposal: Optional[str] = None
    confidence: float = Field(ge=0, le=1)
    timestamp: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "agent_name": "Workout Modification Agent",
                "stance": "challenge",
                "reasoning": "User has shoulder injury, overhead press is risky",
                "concerns": ["Joint stress on injured shoulder", "Risk of re-injury"],
                "counter_proposal": "Replace with lateral raises at 50% weight",
                "confidence": 0.9,
                "timestamp": "2025-01-02T10:30:00Z"
            }
        }


# ============================================================================
# DEBATE THREAD SCHEMAS
# ============================================================================

class DebateThreadResponse(BaseModel):
    """Complete debate thread with all agent positions"""
    debate_id: str
    topic: str
    initial_proposal: Dict[str, Any]
    agent_positions: List[AgentPositionResponse]
    consensus_reached: bool
    final_decision: Optional[Dict[str, Any]] = None
    debate_duration_seconds: float
    agents_participated: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "debate_id": "debate_123_20250102",
                "topic": "Modify workout due to user fatigue",
                "initial_proposal": {
                    "action": "Reduce workout by 40%",
                    "reason": "User slept 4 hours"
                },
                "agent_positions": [],
                "consensus_reached": True,
                "final_decision": {"action": "Reduce by 50%", "votes": 4},
                "debate_duration_seconds": 2.5,
                "agents_participated": 5
            }
        }


# ============================================================================
# LIVE DEBATE EVENT (For WebSocket)
# ============================================================================

class LiveDebateEvent(BaseModel):
    """
    Real-time debate event sent via WebSocket.
    Allows user to watch agents debate in real-time.
    """
    event_type: str  # "agent_position", "consensus", "final_decision"
    debate_id: str
    agent_name: Optional[str] = None
    data: Dict[str, Any]
    timestamp: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "event_type": "agent_position",
                "debate_id": "debate_123",
                "agent_name": "Sleep Agent",
                "data": {
                    "stance": "support",
                    "reasoning": "User needs recovery"
                },
                "timestamp": "2025-01-02T10:30:00Z"
            }
        }


# ============================================================================
# DECISION TIMELINE
# ============================================================================

class DecisionTimelineResponse(BaseModel):
    """
    Timeline of how decision was made.
    Shows step-by-step agent interactions.
    """
    debate_id: str
    timeline: List[Dict[str, Any]]
    total_steps: int
    duration_seconds: float
    
    class Config:
        json_schema_extra = {
            "example": {
                "debate_id": "debate_123",
                "timeline": [
                    {
                        "step": 1,
                        "timestamp": "2025-01-02T10:30:00Z",
                        "agent": "Workout Modification Agent",
                        "action": "Proposed reduction",
                        "reasoning": "Safety first"
                    },
                    {
                        "step": 2,
                        "timestamp": "2025-01-02T10:30:01Z",
                        "agent": "Sleep Agent",
                        "action": "Supported proposal",
                        "reasoning": "User needs recovery"
                    }
                ],
                "total_steps": 5,
                "duration_seconds": 2.3
            }
        }


# ============================================================================
# MAIN DEBATE RESPONSE
# ============================================================================

class DebateResponse(BaseModel):
    """
    Complete debate response.
    This is what users see - full transparency of AI decision-making.
    """
    debate_id: str
    triggered_by: str  # "intervention", "workout_modification", "user_request"
    topic: str
    
    # The debate
    debate_thread: DebateThreadResponse
    
    # The decision
    final_decision: Dict[str, Any]
    consensus_level: float = Field(ge=0, le=1, description="Agreement level: 0=split, 1=unanimous")
    
    # Transparency
    decision_rationale: str
    dissenting_opinions: List[Dict[str, Any]] = []
    
    # Metadata
    started_at: str
    completed_at: str
    total_duration_seconds: float
    
    class Config:
        json_schema_extra = {
            "example": {
                "debate_id": "debate_user123_20250102103045",
                "triggered_by": "intervention",
                "topic": "Should we reduce user's workout intensity?",
                "debate_thread": {
                    "debate_id": "debate_user123_20250102103045",
                    "topic": "Workout intensity adjustment",
                    "initial_proposal": {
                        "action": "Reduce workout by 40%",
                        "proposed_by": "Workout Modification Agent"
                    },
                    "agent_positions": [
                        {
                            "agent_name": "Sleep Agent",
                            "stance": "support",
                            "reasoning": "User slept only 4 hours",
                            "concerns": [],
                            "confidence": 0.95,
                            "timestamp": "2025-01-02T10:30:45Z"
                        }
                    ],
                    "consensus_reached": True,
                    "final_decision": {"action": "Reduce by 50%"},
                    "debate_duration_seconds": 2.1,
                    "agents_participated": 4
                },
                "final_decision": {
                    "action": "reduce_intensity",
                    "modification": "50% reduction in sets and weight",
                    "reasoning": "Consensus: user needs recovery",
                    "approved_by": 4,
                    "challenged_by": 0
                },
                "consensus_level": 1.0,
                "decision_rationale": "All 4 agents agreed that poor sleep requires significant reduction",
                "dissenting_opinions": [],
                "started_at": "2025-01-02T10:30:45Z",
                "completed_at": "2025-01-02T10:30:47Z",
                "total_duration_seconds": 2.1
            }
        }


# ============================================================================
# REQUEST SCHEMAS
# ============================================================================

class TriggerDebateRequest(BaseModel):
    """Request to trigger a debate"""
    topic: str
    initial_proposal: Dict[str, Any]
    context: Dict[str, Any] = {}
    agents_to_include: Optional[List[str]] = None  # If None, use all relevant agents
    
    class Config:
        json_schema_extra = {
            "example": {
                "topic": "Modify workout for injured user",
                "initial_proposal": {
                    "action": "Replace overhead press with lateral raises",
                    "reason": "Shoulder injury"
                },
                "context": {
                    "user_id": 123,
                    "workout_id": 456,
                    "injury": "shoulder impingement"
                },
                "agents_to_include": ["Workout Modification Agent", "Injury Prevention Agent"]
            }
        }


class DebateHistoryResponse(BaseModel):
    """User's debate history"""
    user_id: int
    total_debates: int
    debates: List[Dict[str, Any]]
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 123,
                "total_debates": 5,
                "debates": [
                    {
                        "debate_id": "debate_123_20250102",
                        "topic": "Workout modification",
                        "consensus_level": 0.8,
                        "timestamp": "2025-01-02T10:30:00Z"
                    }
                ]
            }
        }