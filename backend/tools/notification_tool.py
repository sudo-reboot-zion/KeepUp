"""
Notification Tool
Handles sending notifications to the user via various channels.
"""
from typing import Dict, Any, Optional

class NotificationTool:
    """
    Sends notifications to the user (Push, Email, In-App).
    """
    
    async def send_notification(
        self, 
        user_id: int, 
        title: str, 
        body: str, 
        channel: str = "in_app",
        priority: str = "normal",
        data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Send a notification, respecting user preferences.
        """
        from core.database import async_session_factory
        from services.notification_service import NotificationService
        from models.user import User
        from sqlalchemy import select
        
        async with async_session_factory() as db:
            # 1. Fetch User Preferences
            result = await db.execute(select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()
            
            if not user:
                return False
                
            prefs = user.notification_preferences or {}
            notif_type = data.get("type", "general") if data else "general"
            
            # 2. Check if allowed
            if not NotificationService.should_send_notification(prefs, notif_type, priority):
                print(f"🔕 Notification blocked by user preferences: {title}")
                return False
            
            # 3. Send via NotificationService (DB + WebSocket)
            # This handles saving to DB and emitting via WebSocket if online
            await NotificationService.create_intervention_notification(
                user_id=user_id,
                intervention_type=data.get("type", "general") if data else "general",
                message=body,
                actions_taken=data.get("actions", []) if data else [],
                db=db
            )
            
            return True

    async def send_morning_briefing(self, user_id: int, briefing_text: str) -> bool:
        """
        Send the daily morning briefing.
        """
        return await self.send_notification(
            user_id=user_id,
            title="🌅 Your Daily Plan",
            body=briefing_text[:100] + "...",  # Preview
            channel="push",
            priority="high",
            data={"type": "morning_briefing", "full_text": briefing_text}
        )

notification_tool = NotificationTool()
