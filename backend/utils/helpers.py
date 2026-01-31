def calculate_user_metrics(user: User, workout_history: list) -> Dict[str, Any]:
    """Calculate intervention-relevant metrics for a user"""
    
    # Count missed workouts in last 7 days
    last_7_days = workout_history[-7:] if len(workout_history) >= 7 else workout_history
    completed_last_week = sum(1 for w in last_7_days if w.get("completed", False))
    
    # Target workouts per week (from user's resolution)
    target_per_week = user.resolution.get("weekly_target", 3)
    if isinstance(target_per_week, str):
        target_per_week = int(target_per_week.split("x")[0])
    
    # Calculate consecutive skips
    consecutive_skips = 0
    for workout in reversed(workout_history):
        if not workout.get("completed", False):
            consecutive_skips += 1
        else:
            break
    
    # Days since last workout
    last_completed = None
    for workout in reversed(workout_history):
        if workout.get("completed", False):
            last_completed = workout.get("completed_date")
            break
    
    if last_completed:
        days_inactive = (datetime.utcnow() - last_completed).days
    else:
        days_inactive = 14  # No workouts in last 2 weeks
    
    # Calculate current week of resolution
    resolution_start = user.resolution.get("start_date")
    if resolution_start:
        weeks_elapsed = (datetime.utcnow() - resolution_start).days // 7 + 1
    else:
        weeks_elapsed = 1
    
    # Calculate abandonment probability (simple heuristic)
    abandonment_prob = 0.0
    
    # Week 3-4 is high risk
    if 3 <= weeks_elapsed <= 4:
        abandonment_prob += 0.3
    
    # Consecutive skips
    if consecutive_skips >= 3:
        abandonment_prob += 0.4
    
    # Low adherence
    adherence = completed_last_week / target_per_week if target_per_week > 0 else 0
    if adherence < 0.5:
        abandonment_prob += 0.3
    
    abandonment_prob = min(1.0, abandonment_prob)
    
    return {
        "user_id": user.id,
        "current_week": weeks_elapsed,
        "completed_last_week": completed_last_week,
        "target_per_week": target_per_week,
        "adherence_rate": adherence,
        "consecutive_skips": consecutive_skips,
        "days_inactive": days_inactive,
        "abandonment_probability": abandonment_prob
    }


def should_trigger_intervention(metrics: Dict[str, Any]) -> tuple[bool, str]:
    """
    Determine if user needs intervention and why.
    
    Returns:
        (needs_intervention: bool, reason: str)
    """
    
    # Criterion 1: 3+ consecutive skips
    if metrics["consecutive_skips"] >= 3:
        return True, "consecutive_skips"
    
    # Criterion 2: Week 3-4 with low adherence
    if 3 <= metrics["current_week"] <= 4 and metrics["adherence_rate"] < 0.6:
        return True, "week_3_pattern"
    
    # Criterion 3: High abandonment probability
    if metrics["abandonment_probability"] > 0.6:
        return True, "abandonment_risk"
    
    # Criterion 4: Extended inactivity
    if metrics["days_inactive"] > 5:
        return True, "extended_inactivity"
    
    return False, ""


async def trigger_intervention_for_user(
    user_id: int,
    reason: str,
    metrics: Dict[str, Any],
    db: AsyncSession
):
    """
    Actually trigger intervention workflow for a user.
    Runs as background task.
    """
    try:
        from services.user_service import UserService
        
        user_profile = await UserService.get_user_profile(user_id, db)
        
        initial_state = {
            "user_id": user_id,
            "trigger_reason": reason,
            "missed_workouts": metrics["target_per_week"] - metrics["completed_last_week"],
            "days_inactive": metrics["days_inactive"],
            "abandonment_probability": metrics["abandonment_probability"],
            "current_week": metrics["current_week"],
            "user_profile": user_profile,
            "errors": []
        }
        
        # Run intervention workflow
        workflow = InterventionWorkflow()
        result = await workflow.run(initial_state, db)
        
        # Send notification to user
        user_message = _build_user_message(
            trigger_reason=reason,
            barriers=result.get("detected_barriers", []),
            actions=result.get("autonomous_actions_taken", []),
            suggestions=result.get("alternative_plans", [])
        )
        
        # TODO: Send actual notification
        print(f"📢 Intervention triggered for user {user_id}: {reason}")
        print(f"Message: {user_message[:100]}...")
        
        # TODO: Save intervention record to database
        # await InterventionService.save(user_id, result, db)
        
    except Exception as e:
        print(f"Failed to trigger intervention for user {user_id}: {e}")