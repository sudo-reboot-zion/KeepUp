"""
WebSocket Connection Manager for real-time social features
"""
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List, Set
import json
from datetime import datetime


class ConnectionManager:
    """Manages WebSocket connections for real-time updates"""
    
    def __init__(self):
        # user_id -> list of websocket connections
        self.active_connections: Dict[int, List[WebSocket]] = {}
        # group_id -> set of user_ids
        self.group_subscriptions: Dict[int, Set[int]] = {}
    
    async def connect(self, user_id: int, websocket: WebSocket):
        """Accept and store a new websocket connection"""
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
        print(f"✓ User {user_id} connected via WebSocket")
    
    def disconnect(self, user_id: int, websocket: WebSocket):
        """Remove a websocket connection"""
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        print(f"✓ User {user_id} disconnected from WebSocket")
    
    async def send_to_user(self, user_id: int, message: dict):
        """Send a message to a specific user (all their connections)"""
        if user_id in self.active_connections:
            message_json = json.dumps({
                **message,
                "timestamp": datetime.now().isoformat()
            })
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_text(message_json)
                except Exception as e:
                    print(f"Error sending to user {user_id}: {e}")
    
    async def broadcast_to_group(self, group_id: int, message: dict, exclude_user: int = None):
        """Broadcast a message to all members of a group"""
        if group_id in self.group_subscriptions:
            for user_id in self.group_subscriptions[group_id]:
                if user_id != exclude_user:
                    await self.send_to_user(user_id, message)
    
    def subscribe_to_group(self, group_id: int, user_id: int):
        """Subscribe a user to a group's updates"""
        if group_id not in self.group_subscriptions:
            self.group_subscriptions[group_id] = set()
        self.group_subscriptions[group_id].add(user_id)
    
    def unsubscribe_from_group(self, group_id: int, user_id: int):
        """Unsubscribe a user from a group's updates"""
        if group_id in self.group_subscriptions:
            self.group_subscriptions[group_id].discard(user_id)
            if not self.group_subscriptions[group_id]:
                del self.group_subscriptions[group_id]


# Global instance
manager = ConnectionManager()
