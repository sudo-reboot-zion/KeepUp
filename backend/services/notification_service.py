# services/notification_service.py

"""
Notification Service - In-App + WebSocket
Stores notifications in database and sends real-time via WebSocket
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func


class NotificationService:
    """
    Simple notification system:
    1. Save to database (persistent)
    2. Send via WebSocket if user online (real-time)
    """
    
    @staticmethod
    def should_send_notification(
        user_preferences: Dict[str, Any],
        notification_type: str,
        priority: str = "normal"
    ) -> bool:
        """
        Check if notification should be sent based on user preferences.
        """
        if not user_preferences:
            return True  # Default to allow if no prefs set
            
        # 1. Check Global Pause (Vacation/Sick Mode)
        paused_until = user_preferences.get("paused_until")
        if paused_until:
            if datetime.fromisoformat(paused_until) > datetime.utcnow():
                return False
        
        # 2. Check Specific Type
        # Map internal types to preference keys
        type_map = {
            "morning_briefing": "morning_briefing",
            "evening_checkin": "evening_wind_down",
            "workout_reminder": "workout_reminders",
            "milestone": "milestones"
        }
        
        pref_key = type_map.get(notification_type)
        if pref_key:
            setting = user_preferences.get(pref_key, {})
            if isinstance(setting, dict) and not setting.get("enabled", True):
                return False
        
        # 3. Check Quiet Hours (unless high priority)
        if priority != "high":
            quiet_hours = user_preferences.get("quiet_hours", {})
            start = quiet_hours.get("start")
            end = quiet_hours.get("end")
            
            if start and end:
                now_time = datetime.now().strftime("%H:%M")
                # Handle overnight range (e.g. 22:00 to 06:00)
                if start > end:
                    if now_time >= start or now_time <= end:
                        return False
                # Handle same day range (e.g. 09:00 to 17:00 - unlikely for quiet hours but possible)
                else:
                    if start <= now_time <= end:
                        return False
                        
        return True

    @staticmethod
    async def send_intervention_notification(
        user_id: int,
        intervention_plan: Dict[str, Any],
        db: AsyncSession
    ):
        """
        Bridge method for InterventionMonitor.
        Extracts data from intervention_plan and calls create_intervention_notification.
        """
        # Extract data from plan
        autonomous_actions = intervention_plan.get("autonomous_actions", [])
        
        # Build message
        if autonomous_actions:
            action_desc = autonomous_actions[0].get("action", "made some adjustments")
            message = f"I've {action_desc} to help you stay on track."
        else:
            message = "I've noticed you're struggling. Let's look at some ways to get back on track."
            
        return await NotificationService.create_intervention_notification(
            user_id=user_id,
            intervention_type="autonomous_adjustment",
            message=message,
            actions_taken=autonomous_actions,
            db=db
        )
    
    @staticmethod
    async def create_intervention_notification(
        user_id: int,
        intervention_type: str,
        message: str,
        actions_taken: List[Dict[str, Any]],
        db: AsyncSession
    ):
        """
        Create intervention notification.
        Saves to DB and sends via WebSocket if user is online.
        
        Returns: Notification object
        """
        try:
            # Import here to avoid circular imports
            from models.notification import Notification
            
            # Create notification in database
            notification = Notification(
                user_id=user_id,
                type="intervention",
                category="ai_coach",
                title="Your AI Coach Made Adjustments",
                message=message,
                data={
                    "intervention_type": intervention_type,
                    "actions": actions_taken,
                    "timestamp": datetime.utcnow().isoformat()
                },
                priority="high",
                read=False,
                created_at=datetime.utcnow()
            )
            
            db.add(notification)
            await db.commit()
            await db.refresh(notification)
            
            # Send via WebSocket if user is online
            try:
                # Import inside method to avoid circular imports
                from core.websocket import send_notification_to_user
                
                await send_notification_to_user(user_id, {
                    "id": notification.id,
                    "title": notification.title,
                    "message": notification.message,
                    "type": notification.type,
                    "data": notification.data,
                    "created_at": notification.created_at.isoformat()
                })
            except ImportError:
                print("⚠️ WebSocket module not available - skipping real-time send")
            except Exception as ws_error:
                # WebSocket failed but notification is saved in DB
                print(f"⚠️ WebSocket send failed (notification saved): {ws_error}")
            
            print(f"✅ Notification created for user {user_id}")
            return notification
            
        except Exception as e:
            print(f"❌ Failed to create notification: {e}")
            await db.rollback()
            raise
    
    @staticmethod
    async def get_unread_notifications(
        user_id: int,
        db: AsyncSession,
        limit: int = 10
    ) -> List:
        """Get user's unread notifications"""
        from models.notification import Notification
        
        stmt = (
            select(Notification)
            .where(Notification.user_id == user_id, Notification.read == False)
            .order_by(Notification.created_at.desc())
            .limit(limit)
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())
    
    @staticmethod
    async def get_all_notifications(
        user_id: int,
        db: AsyncSession,
        limit: int = 50
    ) -> List:
        """Get all user notifications (for profile/history page)"""
        from models.notification import Notification
        
        stmt = (
            select(Notification)
            .where(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
            .limit(limit)
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())
    
    @staticmethod
    async def mark_as_read(
        notification_id: int,
        user_id: int,
        db: AsyncSession
    ) -> bool:
        """Mark single notification as read"""
        from models.notification import Notification
        
        stmt = (
            update(Notification)
            .where(
                Notification.id == notification_id,
                Notification.user_id == user_id
            )
            .values(read=True, read_at=datetime.utcnow())
        )
        await db.execute(stmt)
        await db.commit()
        return True
    
    @staticmethod
    async def mark_all_as_read(
        user_id: int,
        db: AsyncSession
    ) -> int:
        """Mark all notifications as read, returns count updated"""
        from models.notification import Notification
        
        stmt = (
            update(Notification)
            .where(Notification.user_id == user_id, Notification.read == False)
            .values(read=True, read_at=datetime.utcnow())
        )
        result = await db.execute(stmt)
        await db.commit()
        return result.rowcount
    
    @staticmethod
    async def get_unread_count(
        user_id: int,
        db: AsyncSession
    ) -> int:
        """Get count of unread notifications (for badge)"""
        from models.notification import Notification
        
        stmt = (
            select(func.count())
            .select_from(Notification)
            .where(Notification.user_id == user_id, Notification.read == False)
        )
        result = await db.execute(stmt)
        return result.scalar() or 0