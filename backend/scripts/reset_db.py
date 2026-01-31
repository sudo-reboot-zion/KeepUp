#!/usr/bin/env python

import sys
import os

# Add the backend directory to Python path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

import asyncio
from core.database import drop_db, init_db

async def reset_database():
    # Drop all tables
    await drop_db()
    
    # Create all tables
    await init_db()
    
    print("Database reset completed!")

if __name__ == "__main__":
    asyncio.run(reset_database())
