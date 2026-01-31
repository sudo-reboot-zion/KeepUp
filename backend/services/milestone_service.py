"""
Milestone Detection Service
Automatically detects and awards user milestones
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from datetime import datetime, timedelta
from typing import List, Dict

from models.user import User
from models.daily_log import UserDailyLog, DailyTask
# from models.social import Milestone, GroupMembership, SupportGroup
# from ws.connection_manager import manager


class MilestoneDetector:
    """Detects and awards user milestones"""
    
    MILESTONE_TYPES = {
        "7_day_streak": {
            "name": "7-Day Streak",
            "description": "Completed check-ins for 7 consecutive days",
            "emoji": "🔥"
        },
        "30_day_streak": {
            "name": "30-Day Warrior",
            "description": "Completed check-ins for 30 consecutive days",
            "emoji": "💪"
        },
        "first_checkin": {
            "name": "Getting Started",
            "description": "Completed your first daily check-in",
            "emoji": "🎯"
        },
        "10_workouts": {
            "name": "Workout Rookie",
            "description": "Completed 10 workouts",
            "emoji": "🏋️"
        },
        "30_workouts": {
            "name": "Fitness Enthusiast",
            "description": "Completed 30 workouts",
            "emoji": "💯"
        },
        "100_workouts": {
            "name": "Workout Legend",
            "description": "Completed 100 workouts",
            "emoji": "🏆"
        },
    }
    
    async def check_user_milestones(self, user_id: int, db: AsyncSession) -> List[str]:
        """Check and award milestones for a user"""
        new_milestones = []
        
        # Check streak milestones
        streak = await self._get_current_streak(user_id, db)
        if streak == 7:
            if await self._award_milestone(user_id, "7_day_streak", db):
                new_milestones.append("7_day_streak")
        elif streak == 30:
            if await self._award_milestone(user_id, "30_day_streak", db):
                new_milestones.append("30_day_streak")
        
        # Check workout count milestones
        workout_count = await self._get_workout_count(user_id, db)
        if workout_count == 10:
            if await self._award_milestone(user_id, "10_workouts", db):
                new_milestones.append("10_workouts")
        elif workout_count == 30:
            if await self._award_milestone(user_id, "30_workouts", db):
                new_milestones.append("30_workouts")
        elif workout_count == 100:
            if await self._award_milestone(user_id, "100_workouts", db):
                new_milestones.append("100_workouts")
        
        return new_milestones
    
    async def _get_current_streak(self, user_id: int, db: AsyncSession) -> int:
        """Calculate user's current check-in streak"""
        # Get all check-ins ordered by date descending
        query = select(UserDailyLog.date).where(
            UserDailyLog.user_id == user_id
        ).order_by(UserDailyLog.date.desc())
        
        result = await db.execute(query)
        dates = [row[0] for row in result.all()]
        
        if not dates:
            return 0
        
        # Count consecutive days from today
        streak = 0
        current_date = datetime.now().date()
        
        for date in dates:
            if date == current_date - timedelta(days=streak):
                streak += 1
            else:
                break
        
        return streak
    
    async def _get_workout_count(self, user_id: int, db: AsyncSession) -> int:
        """Get total number of completed workout tasks"""
        query = select(func.count()).select_from(DailyTask).where(
            and_(
                DailyTask.user_id == user_id,
                DailyTask.task_type == "workout",
                DailyTask.is_completed == True
            )
        )
        result = await db.execute(query)
        return result.scalar() or 0
    
    async def _award_milestone(self, user_id: int, milestone_type: str, db: AsyncSession) -> bool:
        """Award a milestone if not already awarded"""
        # Check if already awarded
        query = select(Milestone).where(
            and_(
                Milestone.user_id == user_id,
                Milestone.milestone_type == milestone_type
            )
        )
        result = await db.execute(query)
        existing = result.scalar_one_or_none()
        
        if existing:
            return False
        
        # Award milestone
        milestone = Milestone(
            user_id=user_id,
            milestone_type=milestone_type,
            is_celebrated=False
        )
        db.add(milestone)
        await db.commit()
        
        return True
    
    async def celebrate_milestones(self, db: AsyncSession):
        """Send celebration notifications for uncelebrated milestones"""
        # Get uncelebrated milestones
        query = select(Milestone, User).join(
            User, Milestone.user_id == User.id
        ).where(
            Milestone.is_celebrated == False
        )
        
        result = await db.execute(query)
        rows = result.all()
        
        for milestone, user in rows:
            milestone_info = self.MILESTONE_TYPES.get(milestone.milestone_type, {})
            
            # Notify user via websocket
            await manager.send_to_user(user.id, {
                "type": "milestone_achieved",
                "data": {
                    "milestone_type": milestone.milestone_type,
                    "name": milestone_info.get("name", "Achievement"),
                    "description": milestone_info.get("description", ""),
                    "emoji": milestone_info.get("emoji", "🎉")
                }
            })
            
            # Notify user's groups
            await self._notify_groups(user.id, milestone_info, db)
            
            # Mark as celebrated
            milestone.is_celebrated = True
        
        await db.commit()
    
    async def _notify_groups(self, user_id: int, milestone_info: Dict, db: AsyncSession):
        """Notify user's support groups about milestone"""
        # Get user's groups
        query = select(GroupMembership.group_id).where(
            and_(
                GroupMembership.user_id == user_id,
                GroupMembership.left_at.is_(None)
            )
        )
        result = await db.execute(query)
        group_ids = [row[0] for row in result.all()]
        
        # Get user info
        user_query = select(User).where(User.id == user_id)
        user_result = await db.execute(user_query)
        user = user_result.scalar_one_or_none()
        
        if not user:
            return
        
        # Broadcast to each group
        for group_id in group_ids:
            await manager.broadcast_to_group(group_id, {
                "type": "group_milestone",
                "data": {
                    "user_id": user_id,
                    "display_name": user.display_name,
                    "milestone": milestone_info.get("name", "Achievement"),
                    "emoji": milestone_info.get("emoji", "🎉")
                }
            })


# Global instance
milestone_detector = MilestoneDetector()
