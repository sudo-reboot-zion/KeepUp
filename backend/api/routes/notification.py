from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from api.dependencies import get_current_user
from models.user import User
from services.notification_service import NotificationService
from schemas.notification_schema import (
    NotificationResponse, 
    NotificationListResponse, 
    NotificationCountResponse,
    MarkReadResponse
)

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("", response_model=NotificationListResponse)
async def get_notifications(
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all notifications for the current user.
    """
    notifications = await NotificationService.get_all_notifications(
        user_id=current_user.id,
        db=db,
        limit=limit
    )
    unread_count = await NotificationService.get_unread_count(
        user_id=current_user.id,
        db=db
    )
    return {
        "notifications": notifications,
        "unread_count": unread_count
    }


@router.get("/unread", response_model=List[NotificationResponse])
async def get_unread_notifications(
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get unread notifications for the current user.
    """
    return await NotificationService.get_unread_notifications(
        user_id=current_user.id,
        db=db,
        limit=limit
    )


@router.get("/count", response_model=NotificationCountResponse)
async def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get unread notification count.
    """
    count = await NotificationService.get_unread_count(
        user_id=current_user.id,
        db=db
    )
    return {"count": count}


@router.post("/{notification_id}/read", response_model=MarkReadResponse)
async def mark_as_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Mark a single notification as read.
    """
    success = await NotificationService.mark_as_read(
        notification_id=notification_id,
        user_id=current_user.id,
        db=db
    )
    return {"success": success}


@router.post("/read-all", response_model=MarkReadResponse)
async def mark_all_as_read(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Mark all notifications as read.
    """
    count = await NotificationService.mark_all_as_read(
        user_id=current_user.id,
        db=db
    )
    return {"success": True, "count": count}
