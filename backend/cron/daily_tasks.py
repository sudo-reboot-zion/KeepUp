"""
Daily Cron Jobs
Automated tasks that run on a schedule
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from sqlalchemy import select

from core.database import get_db_session
from models.user import User
from services.milestone_service import milestone_detector


class DailyCronJobs:
    """Manages scheduled background tasks"""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self._setup_jobs()
    
    def _setup_jobs(self):
        """Configure all scheduled jobs"""
        
        # Daily milestone check at 6 AM
        self.scheduler.add_job(
            self.check_all_milestones,
            CronTrigger(hour=6, minute=0),
            id="daily_milestone_check",
            name="Check and award user milestones",
            replace_existing=True
        )
        
        # Celebrate milestones every hour
        self.scheduler.add_job(
            self.celebrate_milestones,
            CronTrigger(minute=0),
            id="hourly_celebration",
            name="Send milestone celebration notifications",
            replace_existing=True
        )
        
        # Daily streak reminder at 8 PM
        self.scheduler.add_job(
            self.send_streak_reminders,
            CronTrigger(hour=20, minute=0),
            id="daily_streak_reminder",
            name="Remind users to maintain streak",
            replace_existing=True
        )
    
    async def check_all_milestones(self):
        """Check milestones for all active users"""
        print(f"[{datetime.now()}] Running daily milestone check...")
        
        async with get_db_session() as db:
            # Get all users who completed onboarding
            query = select(User).where(User.has_completed_onboarding == True)
            result = await db.execute(query)
            users = result.scalars().all()
            
            total_milestones = 0
            for user in users:
                new_milestones = await milestone_detector.check_user_milestones(user.id, db)
                total_milestones += len(new_milestones)
                
                if new_milestones:
                    print(f"  ✓ User {user.id} earned {len(new_milestones)} milestone(s)")
            
            print(f"  Total: {total_milestones} new milestones awarded")
    
    async def celebrate_milestones(self):
        """Send celebration notifications for uncelebrated milestones"""
        async with get_db_session() as db:
            await milestone_detector.celebrate_milestones(db)
    
    async def send_streak_reminders(self):
        """Remind users who haven't checked in today"""
        print(f"[{datetime.now()}] Sending streak reminders...")
        
        async with get_db_session() as db:
            from models.daily_log import UserDailyLog
            from datetime import date
            from ws.connection_manager import manager
            
            # Get all active users
            query = select(User).where(User.has_completed_onboarding == True)
            result = await db.execute(query)
            users = result.scalars().all()
            
            today = date.today()
            reminded = 0
            
            for user in users:
                # Check if user has checked in today
                checkin_query = select(UserDailyLog).where(
                    UserDailyLog.user_id == user.id,
                    UserDailyLog.date == today
                )
                checkin_result = await db.execute(checkin_query)
                checkin = checkin_result.scalar_one_or_none()
                
                if not checkin:
                    # Send reminder via websocket
                    await manager.send_to_user(user.id, {
                        "type": "streak_reminder",
                        "data": {
                            "message": "Don't break your streak! Complete your daily check-in.",
                            "emoji": "⏰"
                        }
                    })
                    reminded += 1
            
            print(f"  Sent {reminded} streak reminders")
    
    def start(self):
        """Start the scheduler"""
        if not self.scheduler.running:
            self.scheduler.start()
            print("✅ Cron jobs started")
            print(f"  - Daily milestone check: 6:00 AM")
            print(f"  - Hourly celebrations: Every hour")
            print(f"  - Streak reminders: 8:00 PM")
    
    def stop(self):
        """Stop the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            print("✅ Cron jobs stopped")


# Global instance
daily_cron = DailyCronJobs()
