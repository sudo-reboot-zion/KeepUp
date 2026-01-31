from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from api.routes import (
    user_route, auth,
    onboarding, resolution, dashboard,
    daily, workout,
    chat,
    checkin,
    nutrition, calendar,
    biometric, life_events,
    progress, intervention, notification,
    safety,
    community
)
from core.config import settings 
from core.database import init_db, close_db
# from fastapi import WebSocket, WebSocketDisconnect  # Websocket for social features - commented out
from core.websocket import socketio_app  # Websocket for real-time notifications
from background_tasks.intervention_monitor import intervention_monitor
import models  



@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    # Startup
    print(f" Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    await init_db()
    print("✅ Database initialized")
    
    # Start background jobs
    intervention_monitor.start()
    print("✅ Background jobs started")

    yield

    # Shutdown
    print("🛑 Shutting down...")
    intervention_monitor.stop()
    print("✅ Background jobs stopped")
    await close_db()
    print("✅ Database connections closed")





app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered fitness system with 15 specialized agents",
    version=settings.APP_VERSION,
    lifespan=lifespan
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/socket.io", socketio_app)
app.mount("/ws/socket.io", socketio_app)
app.include_router(user_route.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(onboarding.router, prefix="/api")
app.include_router(daily.router, prefix="/api")
app.include_router(workout.router, prefix="/api")
app.include_router(progress.router, prefix="/api")
app.include_router(intervention.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(resolution.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(checkin.router, prefix="/api/checkin", tags=["CheckIn"])
app.include_router(nutrition.router, prefix="/api", tags=["Nutrition"])
app.include_router(calendar.router, prefix="/api", tags=["Calendar"])
app.include_router(biometric.router, prefix="/api", tags=["Biometric"])
app.include_router(life_events.router, prefix="/api", tags=["Life Events"])
app.include_router(safety.router, tags=["Safety & Guardrails"])
app.include_router(notification.router, prefix="/api")
app.include_router(community.router, prefix="/api", tags=["Community"])




@app.get("/", tags=["System"])
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.APP_NAME} API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "status": "/health"
    }


@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }







if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
