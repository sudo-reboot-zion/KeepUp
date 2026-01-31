"""
Resolution Service
Business logic for resolution management
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from datetime import datetime

from models.resolution import Resolution, ResolutionStatus
from workflows.resolution_workflow import ResolutionWorkflow
from services.hierarchy_generator import ResolutionHierarchyGenerator



class ResolutionService:
    """Service for managing user resolutions"""
    
    @staticmethod
    async def create_resolution(
        user_id: int,
        resolution_text: str,
        past_attempts: Optional[str],
        life_constraints: Optional[List[str]],
        db: AsyncSession
    ) -> Resolution:
        """
        Create new resolution using ResolutionWorkflow
        
        Args:
            user_id: User ID
            resolution_text: User's goal
            past_attempts: History of past attempts
            life_constraints: Life barriers
            db: Database session
        
        Returns:
            Created Resolution object
        """
        # Run ResolutionWorkflow to generate AI plan
        workflow = ResolutionWorkflow()
        
        initial_state = {
            "user_id": str(user_id),
            "resolution_text": resolution_text,
            "past_attempts": past_attempts,
            "life_constraints": life_constraints or [],
            "goal_analysis": None,
            "failure_risk": None,
            "final_plan": None,
            "debate_summary": None,
            "confidence_score": None,
            "timestamp": None,
            "errors": []
        }
        
        result = await workflow.run(initial_state, db)
        
        # Check for errors
        if result.get("errors"):
            raise ValueError(f"Workflow errors: {', '.join(result['errors'])}")
        
        # Extract weekly target from plan
        weekly_target = None
        if final_plan := result.get("final_plan"):
            weekly_target_str = final_plan.get("weekly_target", "")
            # Parse "3x/week" -> 3
            if "x" in weekly_target_str:
                try:
                    weekly_target = int(weekly_target_str.split("x")[0])
                except:
                    weekly_target = 3  # Default
        
        # Create resolution in database
        resolution = Resolution(
            user_id=user_id,
            resolution_text=resolution_text,
            past_attempts=past_attempts,
            life_constraints=life_constraints,
            final_plan=result.get("final_plan"),
            debate_summary=result.get("debate_summary"),
            confidence_score=result.get("confidence_score"),
            status=ResolutionStatus.ACTIVE,
            workouts_target=weekly_target
        )
        
        db.add(resolution)
        await db.commit()
        await db.refresh(resolution)
        
        # Generate 52-week hierarchy (quarterly phases, weekly plans, daily workouts)
        try:
            hierarchy = await ResolutionHierarchyGenerator.generate_hierarchy(
                resolution=resolution,
                db=db
            )
            print(f"✅ Generated hierarchy: {hierarchy['total_weeks']} weeks, {hierarchy['total_workouts']} workouts")
        except Exception as e:
            print(f"⚠️  Hierarchy generation warning (non-fatal): {str(e)}")
            # Don't fail resolution creation if hierarchy generation fails
        
        return resolution
    
    @staticmethod
    async def confirm_resolution(
        user_id: int,
        resolution_text: str,
        final_plan: Dict[str, Any],
        db: AsyncSession,
        past_attempts: Optional[str] = None,
        life_constraints: Optional[List[str]] = None,
        debate_summary: Optional[Dict[str, Any]] = None,
        confidence_score: Optional[float] = None
    ) -> Resolution:
        """
        Confirm and save a resolution from an existing plan (skips workflow)
        """
        # Extract weekly target from plan
        weekly_target = None
        if final_plan:
            weekly_target_str = final_plan.get("weekly_target", "")
            # Parse "3x/week" -> 3
            if "x" in weekly_target_str:
                try:
                    weekly_target = int(weekly_target_str.split("x")[0])
                except:
                    weekly_target = 3  # Default
        
        # Create resolution in database
        print(f"Attempting to create resolution for user {user_id}")
        resolution = Resolution(
            user_id=user_id,
            resolution_text=resolution_text,
            past_attempts=past_attempts,
            life_constraints=life_constraints,
            final_plan=final_plan,
            debate_summary=debate_summary,
            confidence_score=confidence_score,
            status=ResolutionStatus.ACTIVE,
            workouts_target=weekly_target
        )
        
        try:
            db.add(resolution)
            print("Added resolution to session")
            await db.commit()
            print("Committed resolution to database")
            await db.refresh(resolution)
            print(f"Refreshed resolution ID: {resolution.id}")
        except Exception as e:
            print(f"❌ Database commit failed: {str(e)}")
            import traceback
            traceback.print_exc()
            raise e
        
        # Generate 52-week hierarchy
        try:
            hierarchy = await ResolutionHierarchyGenerator.generate_hierarchy(
                resolution=resolution,
                db=db
            )
            print(f"✅ Generated hierarchy: {hierarchy['total_weeks']} weeks, {hierarchy['total_workouts']} workouts")
        except Exception as e:
            print(f"⚠️  Hierarchy generation warning (non-fatal): {str(e)}")
        
        return resolution
    
    @staticmethod
    async def get_resolution(
        resolution_id: int,
        user_id: int,
        db: AsyncSession
    ) -> Optional[Resolution]:
        """Get resolution by ID"""
        result = await db.execute(
            select(Resolution).where(
                and_(
                    Resolution.id == resolution_id,
                    Resolution.user_id == user_id
                )
            )
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_active_resolution(
        user_id: int,
        db: AsyncSession
    ) -> Optional[Resolution]:
        """Get user's active resolution"""
        result = await db.execute(
            select(Resolution).where(
                and_(
                    Resolution.user_id == user_id,
                    Resolution.status == ResolutionStatus.ACTIVE
                )
            ).order_by(Resolution.created_at.desc())
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def list_resolutions(
        user_id: int,
        status: Optional[ResolutionStatus],
        db: AsyncSession
    ) -> List[Resolution]:
        """List user's resolutions"""
        conditions = [Resolution.user_id == user_id]
        
        if status:
            conditions.append(Resolution.status == status)
        
        result = await db.execute(
            select(Resolution)
            .where(and_(*conditions))
            .order_by(Resolution.created_at.desc())
        )
        return list(result.scalars().all())
    
    @staticmethod
    async def update_progress(
        resolution_id: int,
        user_id: int,
        workouts_completed: Optional[int],
        current_week: Optional[int],
        adherence_rate: Optional[float],
        streak_days: Optional[int],
        db: AsyncSession
    ) -> Resolution:
        """Update resolution progress"""
        resolution = await ResolutionService.get_resolution(resolution_id, user_id, db)
        
        if not resolution:
            raise ValueError("Resolution not found")
        
        if workouts_completed is not None:
            resolution.workouts_completed = workouts_completed
        
        if current_week is not None:
            resolution.current_week = current_week
        
        if adherence_rate is not None:
            resolution.adherence_rate = adherence_rate
        
        if streak_days is not None:
            resolution.streak_days = streak_days
        
        resolution.updated_at = datetime.utcnow()
        
        await db.commit()
        await db.refresh(resolution)
        
        return resolution
    
    @staticmethod
    async def mark_completed(
        resolution_id: int,
        user_id: int,
        db: AsyncSession
    ) -> Resolution:
        """Mark resolution as completed"""
        resolution = await ResolutionService.get_resolution(resolution_id, user_id, db)
        
        if not resolution:
            raise ValueError("Resolution not found")
        
        resolution.status = ResolutionStatus.COMPLETED
        resolution.completed_at = datetime.utcnow()
        
        await db.commit()
        await db.refresh(resolution)
        
        return resolution
    
    @staticmethod
    async def mark_abandoned(
        resolution_id: int,
        user_id: int,
        db: AsyncSession
    ) -> Resolution:
        """Mark resolution as abandoned"""
        resolution = await ResolutionService.get_resolution(resolution_id, user_id, db)
        
        if not resolution:
            raise ValueError("Resolution not found")
        
        resolution.status = ResolutionStatus.ABANDONED
        resolution.abandoned_at = datetime.utcnow()
        
        await db.commit()
        await db.refresh(resolution)
        
        return resolution
    
    @staticmethod
    async def get_statistics(user_id: int, db: AsyncSession) -> Dict[str, Any]:
        """Get user's resolution statistics"""
        result = await db.execute(
            select(
                func.count(Resolution.id).label("total"),
                func.count(Resolution.id).filter(Resolution.status == ResolutionStatus.ACTIVE).label("active"),
                func.count(Resolution.id).filter(Resolution.status == ResolutionStatus.COMPLETED).label("completed"),
                func.count(Resolution.id).filter(Resolution.status == ResolutionStatus.ABANDONED).label("abandoned")
            ).where(Resolution.user_id == user_id)
        )
        
        stats = result.one()
        
        return {
            "total": stats.total or 0,
            "active": stats.active or 0,
            "completed": stats.completed or 0,
            "abandoned": stats.abandoned or 0,
            "completion_rate": (stats.completed / stats.total * 100) if stats.total > 0 else 0
        }
