"""
Agent Memory System - LangGraph Compatible
Manages persistent memory for what agents learn about users.
Integrates with LangGraph state management.
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
import json


class AgentMemory:
    """
    LangGraph-compatible memory manager.
    
    Memory Flow:
    1. Workflow starts → load_to_state() loads relevant memories into state
    2. Agents execute → use add_learning_to_state() to record new learnings
    3. Workflow ends → persist_from_state() saves updates to database
    
    This design keeps LangGraph state as the source of truth during workflow execution,
    while using the database for long-term persistence across workflows.
    """
    
    @staticmethod
    async def load_to_state(
        user_id: int,
        db: AsyncSession,
        state_type: str,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Load relevant memories from database into workflow state.
        
        Args:
            user_id: User ID
            db: Database session
            state_type: Type of workflow ("onboarding", "daily_check", "intervention")
            filters: Optional filters (e.g., {"learning_type": "failure_pattern"})
        
        Returns:
            Dict with categorized memories ready to add to state
            
        Example:
            memory_data = await AgentMemory.load_to_state(
                user_id=123,
                db=db,
                state_type="daily_check"
            )
            state["user_memory"] = memory_data
        """
        from models.user import UserMemory
        
        # Build query conditions
        conditions = [
            UserMemory.user_id == user_id,
            UserMemory.confidence >= 0.5  # Only confident learnings
        ]
        
        # Filter expired learnings
        conditions.append(
            (UserMemory.expires_at.is_(None)) | 
            (UserMemory.expires_at > datetime.utcnow())
        )
        
        # Apply additional filters
        if filters:
            if "learning_type" in filters:
                conditions.append(UserMemory.learning_type == filters["learning_type"])
            if "agent_name" in filters:
                conditions.append(UserMemory.agent_name == filters["agent_name"])
        
        # Query database
        result = await db.execute(
            select(UserMemory)
            .where(and_(*conditions))
            .order_by(UserMemory.confidence.desc(), UserMemory.updated_at.desc())
        )
        
        memories = result.scalars().all()
        
        # Organize by type for easy access
        memory_data = {
            "by_type": {},
            "by_agent": {},
            "all": []
        }
        
        for m in memories:
            memory_dict = {
                "agent_name": m.agent_name,
                "learning_type": m.learning_type,
                "content": m.content,
                "confidence": m.confidence,
                "created_at": m.created_at.isoformat(),
                "updated_at": m.updated_at.isoformat()
            }
            
            # Add to all
            memory_data["all"].append(memory_dict)
            
            # Group by type
            if m.learning_type not in memory_data["by_type"]:
                memory_data["by_type"][m.learning_type] = []
            memory_data["by_type"][m.learning_type].append(memory_dict)
            
            # Group by agent
            if m.agent_name not in memory_data["by_agent"]:
                memory_data["by_agent"][m.agent_name] = []
            memory_data["by_agent"][m.agent_name].append(memory_dict)
        
        return memory_data
    
    @staticmethod
    async def persist_from_state(
        user_id: int,
        db: AsyncSession,
        memory_updates: List[Dict[str, Any]]
    ):
        """
        Persist memory updates from workflow state to database.
        
        Args:
            user_id: User ID
            db: Database session
            memory_updates: List of learnings from state["memory_updates"]
        
        Example:
            await AgentMemory.persist_from_state(
                user_id=123,
                db=db,
                memory_updates=state.get("memory_updates", [])
            )
        """
        from models.user import UserMemory
        
        if not memory_updates:
            return
        
        for update in memory_updates:
            agent_name = update.get("agent_name")
            learning_type = update.get("learning_type")
            content = update.get("content")
            confidence = update.get("confidence", 1.0)
            expires_after_days = update.get("expires_after_days")
            
            if not all([agent_name, learning_type, content]):
                continue  # Skip invalid updates
            
            # Check if similar learning exists
            existing = await db.execute(
                select(UserMemory).where(
                    and_(
                        UserMemory.user_id == user_id,
                        UserMemory.agent_name == agent_name,
                        UserMemory.learning_type == learning_type
                    )
                )
            )
            existing_memory = existing.scalar_one_or_none()
            
            if existing_memory:
                # Update existing learning
                existing_memory.confidence = min(1.0, existing_memory.confidence + 0.1)
                existing_memory.content = content
                existing_memory.updated_at = datetime.utcnow()
            else:
                # Create new learning
                expires_at = None
                if expires_after_days:
                    expires_at = datetime.utcnow() + timedelta(days=expires_after_days)
                
                memory_entry = UserMemory(
                    user_id=user_id,
                    agent_name=agent_name,
                    learning_type=learning_type,
                    content=content,
                    confidence=confidence,
                    expires_at=expires_at
                )
                
                db.add(memory_entry)
        
        await db.commit()
    
    @staticmethod
    def add_learning_to_state(
        state: Dict[str, Any],
        agent_name: str,
        learning_type: str,
        content: Dict[str, Any],
        confidence: float = 1.0,
        expires_after_days: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Helper for agents to add learnings to state during workflow execution.
        
        Args:
            state: Current workflow state
            agent_name: Which agent learned this
            learning_type: Category (e.g., "failure_pattern", "preference")
            content: The actual learning (JSON-serializable dict)
            confidence: How confident the agent is (0.0-1.0)
            expires_after_days: Auto-delete after N days (None = never expires)
        
        Returns:
            Updated state
            
        Example:
            # Inside an agent's analyze() method
            state = AgentMemory.add_learning_to_state(
                state,
                agent_name="Failure Pattern Agent",
                learning_type="failure_pattern",
                content={
                    "pattern": "quits_week_4",
                    "occurrences": 3,
                    "triggers": ["busy_at_work", "travel"]
                },
                confidence=0.85
            )
        """
        # Initialize memory_updates if not present
        if "memory_updates" not in state or state["memory_updates"] is None:
            state["memory_updates"] = []
        
        # Add new learning
        state["memory_updates"].append({
            "agent_name": agent_name,
            "learning_type": learning_type,
            "content": content,
            "confidence": confidence,
            "expires_after_days": expires_after_days,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        return state
    
    @staticmethod
    def get_memory_from_state(
        state: Dict[str, Any],
        learning_type: Optional[str] = None,
        agent_name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Helper to retrieve memories from state.
        
        Args:
            state: Current workflow state
            learning_type: Filter by type (None = all types)
            agent_name: Filter by agent (None = all agents)
        
        Returns:
            List of matching memories
            
        Example:
            # Get all failure patterns from state
            patterns = AgentMemory.get_memory_from_state(
                state,
                learning_type="failure_pattern"
            )
        """
        user_memory = state.get("user_memory", {})
        
        if learning_type:
            return user_memory.get("by_type", {}).get(learning_type, [])
        elif agent_name:
            return user_memory.get("by_agent", {}).get(agent_name, [])
        else:
            return user_memory.get("all", [])


# Legacy compatibility - keeping for backward compatibility
class LegacyAgentMemory:
    """
    DEPRECATED: Legacy memory interface for backward compatibility.
    New code should use the static methods in AgentMemory class.
    """
    
    def __init__(self, user_id: int, db: AsyncSession):
        self.user_id = user_id
        self.db = db
    
    async def store_learning(
        self,
        agent_name: str,
        learning_type: str,
        content: Dict[str, Any],
        confidence: float = 1.0,
        expires_after_days: Optional[int] = None
    ):
        """Legacy method - use AgentMemory.persist_from_state() instead"""
        await AgentMemory.persist_from_state(
            self.user_id,
            self.db,
            [{
                "agent_name": agent_name,
                "learning_type": learning_type,
                "content": content,
                "confidence": confidence,
                "expires_after_days": expires_after_days
            }]
        )
    
    async def recall(
        self,
        agent_name: Optional[str] = None,
        learning_type: Optional[str] = None,
        min_confidence: float = 0.5
    ) -> List[Dict[str, Any]]:
        """Legacy method - use AgentMemory.load_to_state() instead"""
        filters = {}
        if agent_name:
            filters["agent_name"] = agent_name
        if learning_type:
            filters["learning_type"] = learning_type
        
        memory_data = await AgentMemory.load_to_state(
            self.user_id,
            self.db,
            state_type="legacy",
            filters=filters
        )
        
        # Filter by confidence
        return [m for m in memory_data.get("all", []) if m["confidence"] >= min_confidence]


# Helper function for easy access (legacy compatibility)
async def get_agent_memory(user_id: int, db: AsyncSession) -> LegacyAgentMemory:
    """Factory function to get LegacyAgentMemory instance"""
    return LegacyAgentMemory(user_id, db)
