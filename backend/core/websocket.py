# core/websocket.py
"""
WebSocket Manager - Real-time communication
Handles: notifications, live chat, workout coaching

FIXED: Removed Redis dependency (not needed for single-server deployment)
"""
import socketio
from typing import Dict, Any, Optional, Set
from datetime import datetime
import json
from core.config import settings


# Create Socket.IO server (in-memory manager, no Redis needed)
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*',  # Configure this properly in production
    logger=False,
    engineio_logger=False
    # No client_manager specified = uses default in-memory manager
    # This is fine for single-server deployment
)


class ConnectionManager:
    """
    Manages WebSocket connections for real-time features.
    
    Features:
    - User-specific rooms (notifications, chat)
    - Broadcast capabilities
    - Connection state tracking
    """
    
    def __init__(self):
        # Track active connections: {user_id: {sid1, sid2, ...}}
        self.active_connections: Dict[int, Set[str]] = {}
        
        # Track session data: {sid: {"user_id": 123, "connected_at": ...}}
        self.sessions: Dict[str, Dict[str, Any]] = {}
    
    def add_connection(self, sid: str, user_id: int):
        """Register new connection"""
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        
        self.active_connections[user_id].add(sid)
        self.sessions[sid] = {
            "user_id": user_id,
            "connected_at": datetime.utcnow().isoformat()
        }
        
        print(f"✅ User {user_id} connected (sid: {sid})")
    
    def remove_connection(self, sid: str):
        """Remove connection"""
        if sid in self.sessions:
            user_id = self.sessions[sid]["user_id"]
            
            if user_id in self.active_connections:
                self.active_connections[user_id].discard(sid)
                
                # Remove user entry if no more connections
                if not self.active_connections[user_id]:
                    del self.active_connections[user_id]
            
            del self.sessions[sid]
            print(f"❌ Connection removed (sid: {sid})")
    
    def get_user_sessions(self, user_id: int) -> Set[str]:
        """Get all session IDs for a user"""
        return self.active_connections.get(user_id, set())
    
    def is_user_online(self, user_id: int) -> bool:
        """Check if user is online"""
        return user_id in self.active_connections
    
    def get_online_count(self) -> int:
        """Get total number of online users"""
        return len(self.active_connections)


# Global connection manager
manager = ConnectionManager()


# ============================================================================
# SOCKET.IO EVENT HANDLERS
# ============================================================================

@sio.event
async def connect(sid, environ, auth):
    """
    Handle new WebSocket connection.
    Client must provide JWT token for authentication.
    """
    try:
        # Extract token from auth
        token = auth.get('token') if auth else None
        
        if not token:
            print(f"❌ Connection rejected (sid: {sid}) - No token")
            return False  # Reject connection
        
        # Verify JWT and get user_id
        from core.security import verify_token
        user_id = verify_token(token)
        
        if not user_id:
            print(f"❌ Connection rejected (sid: {sid}) - Invalid token")
            return False
        
        # Register connection
        manager.add_connection(sid, user_id)
        
        # Join user-specific room
        await sio.enter_room(sid, f"user_{user_id}")
        
        # Send welcome message
        await sio.emit('connected', {
            'message': 'Connected to Euexia real-time system',
            'user_id': user_id,
            'timestamp': datetime.utcnow().isoformat()
        }, room=sid)
        
        # Send unread notification count
        from services.notification_service import NotificationService
        from core.database import get_db
        
        async for db in get_db():
            unread_count = await NotificationService.get_unread_count(user_id, db)
            await sio.emit('notification_count', {
                'count': unread_count
            }, room=sid)
            break
        
        print(f"✅ User {user_id} authenticated and connected")
        return True
        
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False


@sio.event
async def disconnect(sid):
    """Handle disconnection"""
    manager.remove_connection(sid)
    print(f"👋 Client disconnected (sid: {sid})")


@sio.event
async def ping(sid, data):
    """Keepalive ping"""
    await sio.emit('pong', {'timestamp': datetime.utcnow().isoformat()}, room=sid)


# ============================================================================
# SERVER-SIDE EMITTERS (Called by backend services)
# ============================================================================

async def send_notification_to_user(user_id: int, notification: Dict[str, Any]):
    """
    Send notification to specific user (all their devices).
    Called by NotificationService when intervention triggers.
    """
    if not manager.is_user_online(user_id):
        print(f"📭 User {user_id} offline, notification saved to DB only")
        return
    
    # Send to all user's connected devices
    await sio.emit('notification', notification, room=f"user_{user_id}")
    print(f"📢 Sent notification to user {user_id}")


async def send_intervention_alert(user_id: int, intervention_data: Dict[str, Any]):
    """
    Send intervention alert to user in real-time.
    Shows modal/banner in app immediately.
    """
    if not manager.is_user_online(user_id):
        return
    
    await sio.emit('intervention_alert', {
        'type': 'autonomous_intervention',
        'title': 'Your AI Coach Made Adjustments',
        'data': intervention_data,
        'timestamp': datetime.utcnow().isoformat()
    }, room=f"user_{user_id}")


async def broadcast_system_message(message: str, priority: str = 'normal'):
    """
    Broadcast message to ALL connected users.
    Used for: maintenance notices, new features, etc.
    """
    await sio.emit('system_message', {
        'message': message,
        'priority': priority,
        'timestamp': datetime.utcnow().isoformat()
    })


# Export for use in FastAPI
socketio_app = socketio.ASGIApp(
    sio,
    socketio_path='',
    other_asgi_app=None  # We'll mount this on FastAPI
)