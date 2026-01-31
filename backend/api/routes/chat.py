# api/routes/chat.py

"""
Chat API Routes
Handles chat history, clearing conversations, etc.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any
from pydantic import BaseModel

from api.dependencies import get_db, get_current_user
from agents.coordination.chat_agent import chat_agent
from models.user import User
from schemas.unified_schema import ChatMessageRequest, ChatMessageResponse

router = APIRouter(prefix="/chat", tags=["chat"])



@router.post("/send", response_model=ChatMessageResponse)
async def send_chat_message(
    request: ChatMessageRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Send message to AI coach (REST API fallback for WebSocket).
    
    Use this when:
    - Testing chat agent
    - WebSocket not available
    - Batch processing messages
    
    For real-time chat, use WebSocket instead.
    """
    try:
        from datetime import datetime
        
        response = await chat_agent.respond(
            user_id=current_user.id,
            message=request.message,
            context=request.context
        )
        
        return ChatMessageResponse(
            message=response["message"],
            data=response.get("data", {}),
            actions=response.get("actions", []),
            confidence=response.get("confidence", 0.8),
            timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat failed: {str(e)}"
        )


@router.get("/history")
async def get_chat_history(
    limit: int = 20,
    current_user: User = Depends(get_current_user)
):
    """
    Get conversation history with AI coach.
    
    Returns last N messages from current session.
    TODO: Store in database for persistence across sessions.
    """
    history = chat_agent._get_conversation_history(current_user.id)
    
    return {
        "user_id": current_user.id,
        "messages": history[-limit:],
        "total": len(history)
    }


@router.delete("/history")
async def clear_chat_history(
    current_user: User = Depends(get_current_user)
):
    """Clear conversation history"""
    chat_agent.clear_history(current_user.id)
    
    return {
        "success": True,
        "message": "Conversation history cleared"
    }


@router.get("/example")
async def get_chat_examples():
    """Example chat messages for testing"""
    return {
        "examples": [
            {
                "message": "How do I do a proper squat?",
                "expected_intent": "workout_question"
            },
            {
                "message": "My shoulder hurts during bench press",
                "expected_intent": "injury_concern"
            },
            {
                "message": "Can I replace deadlifts with something else?",
                "expected_intent": "modification_request"
            },
            {
                "message": "I'm too tired to work out today",
                "expected_intent": "motivation"
            },
            {
                "message": "How am I doing with my progress?",
                "expected_intent": "progress_inquiry"
            }
        ]
    }