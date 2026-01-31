import asyncio
import os
import sys
from dotenv import load_dotenv

# Load environment variables from backend/.env
load_dotenv(os.path.join(os.getcwd(), 'backend', '.env'))

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from models.user import User
from models.resolution import Resolution, ResolutionStatus
from services.resolution_service import ResolutionService
from core.database import Base

DATABASE_URL = "sqlite+aiosqlite:///backend/keepup.db"

async def verify_and_fix():
    engine = create_async_engine(DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as db:
        # Get all users who completed onboarding
        stmt = select(User).where(User.has_completed_onboarding == True)
        result = await db.execute(stmt)
        users = result.scalars().all()
        
        print(f"Checking {len(users)} users who completed onboarding...")
        
        for user in users:
            # Check for active resolution
            stmt = select(Resolution).where(
                Resolution.user_id == user.id,
                Resolution.status == ResolutionStatus.ACTIVE
            )
            result = await db.execute(stmt)
            resolution = result.scalar_one_or_none()
            
            if not resolution:
                print(f"⚠️ User {user.username} (ID: {user.id}) has no active resolution. Fixing...")
                
                # Mock a final plan if missing
                final_plan = {
                    "interpreted_goal": user.primary_goal or "Fitness Mastery",
                    "weekly_target": "3x/week",
                    "first_milestone": "Habit consistency",
                    "reasoning": "Standard plan generated during fix"
                }
                
                try:
                    await ResolutionService.confirm_resolution(
                        user_id=user.id,
                        resolution_text=user.goal_details.get("details", "Fitness Goal") if user.goal_details else "Fitness Goal",
                        final_plan=final_plan,
                        db=db,
                        past_attempts=user.goal_details.get("past_attempts", "") if user.goal_details else "",
                        life_constraints=user.goal_details.get("life_constraints", []) if user.goal_details else [],
                        debate_summary={"summary": "Auto-generated during fix"},
                        confidence_score=0.9
                    )
                    print(f"✅ Created resolution for {user.username}")
                except Exception as e:
                    print(f"❌ Failed to fix {user.username}: {str(e)}")
            else:
                print(f"✅ User {user.username} already has an active resolution.")
        
        await db.commit()

if __name__ == "__main__":
    asyncio.run(verify_and_fix())
