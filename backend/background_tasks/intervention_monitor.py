"""
Intervention Monitor
Autonomous AI system that monitors users for abandonment risk
and triggers interventions proactively
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from core.database import AsyncSessionLocal
from models.resolution import Resolution, ResolutionStatus
from workflows.intervention_workflow import InterventionWorkflow
from services.notification_service import NotificationService

logger = logging.getLogger(__name__)


class InterventionMonitor:
    """
    Monitors users for abandonment risk and triggers interventions.
    
    This is the "killer feature" - AI that acts proactively, not just responds.
    
    Runs every hour to:
    1. Check all active resolutions
    2. Identify at-risk users (low adherence, high abandonment probability)
    3. Run InterventionWorkflow
    4. Apply autonomous protective actions
    5. Send notifications
    """
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.workflow = InterventionWorkflow()
        self.is_running = False
    
    async def check_at_risk_users(self):
        """
        Check all active resolutions for abandonment risk.
        This is the main autonomous intervention logic.
        """
        logger.info("🔍 Intervention Monitor: Checking for at-risk users...")
        
        async with AsyncSessionLocal() as db:
            try:
                # Query at-risk resolutions
                # Criteria: Active status + (low adherence OR high abandonment probability)
                result = await db.execute(
                    select(Resolution).where(
                        and_(
                            Resolution.status == ResolutionStatus.ACTIVE,
                            (
                                (Resolution.adherence_rate < 0.6) |  # Low adherence
                                (Resolution.abandonment_probability > 0.7)  # High risk
                            )
                        )
                    )
                )
                
                at_risk_resolutions = result.scalars().all()
                
                if not at_risk_resolutions:
                    logger.info("✅ No at-risk users found")
                    return
                
                logger.info(f"🚨 Found {len(at_risk_resolutions)} at-risk users")
                
                # Trigger intervention for each at-risk user
                for resolution in at_risk_resolutions:
                    await self._trigger_intervention(resolution, db)
                
                logger.info(f"✅ Intervention check complete. Processed {len(at_risk_resolutions)} users")
                
            except Exception as e:
                logger.error(f"❌ Error checking at-risk users: {e}", exc_info=True)
    
    async def _trigger_intervention(
        self,
        resolution: Resolution,
        db: AsyncSession
    ):
        """
        Trigger intervention for a specific at-risk user.
        
        Runs the InterventionWorkflow which:
        - Detects barriers
        - Assesses motivation
        - Generates intervention options
        - Applies autonomous protective actions
        """
        logger.info(f"🚨 Triggering intervention for user {resolution.user_id} (resolution {resolution.id})")
        
        try:
            # Calculate days inactive (simplified - in production, query last workout)
            days_inactive = 3  # TODO: Calculate from workout history
            
            # Calculate missed workouts
            missed_workouts = max(0, (resolution.workouts_target or 3) - resolution.workouts_completed)
            
            # Prepare intervention state
            initial_state = {
                "user_id": str(resolution.user_id),
                "missed_workouts": missed_workouts,
                "days_inactive": days_inactive,
                "current_week": resolution.current_week,
                "historical_quit_week": None,  # TODO: Get from past resolutions
                "abandonment_probability": resolution.abandonment_probability,
                "detected_barriers": [],
                "motivation_drop": None,
                "intervention_type": None,
                "recommended_actions": None,
                "alternative_plans": None,
                "intervention_plan": None,
                "confidence_score": None,
                "user_memory": None,
                "memory_updates": [],
                "timestamp": None,
                "errors": []
            }
            
            # Run intervention workflow
            logger.info(f"  → Running InterventionWorkflow for user {resolution.user_id}")
            result = await self.workflow.run(initial_state, db)
            
            # Check for errors
            if result.get("errors"):
                logger.error(f"  ❌ Workflow errors: {result['errors']}")
                return
            
            # Update resolution with intervention results
            intervention_plan = result.get("intervention_plan", {})
            autonomous_actions = intervention_plan.get("autonomous_actions", [])
            
            # Update abandonment probability if workflow calculated new value
            if "abandonment_probability" in intervention_plan:
                resolution.abandonment_probability = intervention_plan["abandonment_probability"]
            
            resolution.last_intervention_at = datetime.utcnow()
            
            await db.commit()
            
            logger.info(f"  ✅ Intervention completed. {len(autonomous_actions)} autonomous actions taken")
            
            # Send notification to user
            try:
                await NotificationService.send_intervention_notification(
                    user_id=resolution.user_id,
                    intervention_plan=intervention_plan,
                    db=db
                )
                logger.info(f"  📧 Notification sent to user {resolution.user_id}")
            except Exception as e:
                logger.warning(f"  ⚠️ Failed to send notification: {e}")
            
        except Exception as e:
            logger.error(f"❌ Error triggering intervention for user {resolution.user_id}: {e}", exc_info=True)
    
    def start(self):
        """Start the intervention monitor scheduler"""
        if self.is_running:
            logger.warning("⚠️ Intervention monitor already running")
            return
        
        # Schedule intervention check - runs every hour
        self.scheduler.add_job(
            self.check_at_risk_users,
            'interval',
            hours=1,
            id='intervention_monitor',
            next_run_time=datetime.now(),  # Run immediately on start
            replace_existing=True
        )
        
        self.scheduler.start()
        self.is_running = True
        logger.info("📅 Intervention Monitor started (runs every hour)")
    
    def stop(self):
        """Stop the intervention monitor scheduler"""
        if not self.is_running:
            return
        
        self.scheduler.shutdown(wait=False)
        self.is_running = False
        logger.info("🛑 Intervention Monitor stopped")
    
    def get_status(self):
        """Get current status of the monitor"""
        jobs = self.scheduler.get_jobs() if self.is_running else []
        
        return {
            "running": self.is_running,
            "jobs": [
                {
                    "id": job.id,
                    "next_run": job.next_run_time.isoformat() if job.next_run_time else None,
                    "trigger": str(job.trigger)
                }
                for job in jobs
            ]
        }


# Singleton instance
intervention_monitor = InterventionMonitor()
