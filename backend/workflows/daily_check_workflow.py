"""
Daily Check Workflow - Generates adaptive daily workout plan
Runs every morning to create personalized plan based on user's current state
"""
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from workflows.state import DailyCheckState
from agents.biometric_environment.biometric_agent import BiometricAgent
from agents.biometric_environment.calendar_agent import CalendarAgent
from agents.adaptive_intervention.workout_modification_agent import workout_modification_agent
from agents.adaptive_intervention.sleep_agent import SleepAgent
from agents.mental_wellness.stress_management_agent import StressManagementAgent
from agents.contextual_awareness.barrier_detection_agent import BarrierDetectionAgent

# NEW: Import goal-specific daily plan generators
from workflows.daily_plans import get_plan_generator

from agents.meta_coordinator import MetaCoordinator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func, text
from datetime import date
from services.user_service import UserService
from memory.agent_memory import AgentMemory
# from agents.task_management.task_generation_agent import TaskGenerationAgent
# from agents.occupation.occupation_agent import OccupationAgent
from agents.mental_wellness.emotional_support_agent import EmotionalSupportAgent
from agents.holistic_health_agent import HolisticHealthAgent  # NEW
from models.daily_log import UserDailyLog, DailyTask, TaskType, TaskSource


class DailyCheckWorkflow:
    """
    Orchestrates agents to generate safe, personalized daily workout plan
    """
    
    def __init__(self):
        self.biometric_agent = BiometricAgent()
        self.calendar_agent = CalendarAgent()
        self.workout_mod_agent = workout_modification_agent
        self.sleep_agent = SleepAgent()
        self.stress_agent = StressManagementAgent()
        self.barrier_agent = BarrierDetectionAgent()
        self.occupation_agent = OccupationAgent()
        self.emotional_agent = EmotionalSupportAgent()
        self.holistic_agent = HolisticHealthAgent()  # NEW
        self.task_agent = TaskGenerationAgent()
        self.coordinator = MetaCoordinator()
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(DailyCheckState)
        
        # Add nodes
        workflow.add_node("fetch_profile", self._fetch_user_context)
        workflow.add_node("load_memory", self._load_memory_node)
        workflow.add_node("analyze_biometrics", self._biometric_analysis_node)
        workflow.add_node("analyze_occupation", self._occupation_analysis_node)
        workflow.add_node("analyze_emotions", self._emotional_analysis_node)
        workflow.add_node("analyze_holistic", self._holistic_analysis_node)  # NEW
        workflow.add_node("detect_interventions", self._intervention_detection_node)
        workflow.add_node("detect_barriers", self._barrier_detection_node)
        workflow.add_node("check_schedule", self._schedule_check_node)
        workflow.add_node("generate_workout", self._workout_generation_node)
        workflow.add_node("modify_workout", self._workout_modification_node)
        workflow.add_node("generate_tasks", self._task_generation_node)
        workflow.add_node("save_results", self._save_results_node)
        
        # Define flow
        workflow.set_entry_point("fetch_profile")
        workflow.add_edge("fetch_profile", "load_memory")
        workflow.add_edge("load_memory", "analyze_biometrics")
        workflow.add_edge("analyze_biometrics", "analyze_occupation")
        workflow.add_edge("analyze_occupation", "analyze_emotions")
        workflow.add_edge("analyze_emotions", "analyze_holistic")  # NEW
        workflow.add_edge("analyze_holistic", "detect_interventions")  # NEW
        workflow.add_edge("detect_interventions", "detect_barriers")
        workflow.add_edge("detect_barriers", "check_schedule")
        workflow.add_edge("check_schedule", "generate_workout")
        workflow.add_edge("generate_workout", "modify_workout")
        workflow.add_edge("modify_workout", "generate_tasks")
        workflow.add_edge("generate_tasks", "save_results")
        workflow.add_edge("save_results", END)
        
        return workflow.compile()
    
    async def _fetch_user_context(
        self, 
        state: DailyCheckState,
        db: AsyncSession
    ) -> DailyCheckState:
        """Fetch user profile and recent history"""
        try:
            user_profile = await UserService.get_user_profile(
                int(state["user_id"]), 
                db
            )
            
            # Store in state (internal use)
            state["_user_profile"] = user_profile
            
            # Fetch today's check-in
            today = date.today()
            query = select(UserDailyLog).where(
                and_(UserDailyLog.user_id == int(state["user_id"]), UserDailyLog.date == today)
            )
            result = await db.execute(query)
            checkin = result.scalar_one_or_none()
            
            if checkin:
                state["checkin_data"] = {
                    "sleep_quality": checkin.sleep_quality,
                    "energy_level": checkin.energy_level.value,
                    "soreness_level": checkin.soreness_level.value,
                    "stress_level": checkin.stress_level.value,
                    "notes": checkin.notes
                }
            else:
                state["checkin_data"] = {}
                
            state["current_date"] = today.strftime("%Y-%m-%d")
            
            return state
            
        except Exception as e:
            errors = state.get("errors") or []
            errors.append(f"Profile fetch error: {str(e)}")
            state["errors"] = errors
            return state

    async def _save_results_node(
        self, 
        state: DailyCheckState,
        db: AsyncSession
    ) -> DailyCheckState:
        """Save daily plan and notify user"""
        try:
            # Save to DB (UserDailyLog)
            # ... (existing DB saving logic would go here)
            
            # NEW: Send Morning Briefing via Notification Tool
            from tools.notification_tool import notification_tool
            
            if state.get("morning_briefing"):
                await notification_tool.send_morning_briefing(
                    user_id=int(state["user_id"]),
                    briefing_text=state["morning_briefing"]
                )
            
            return state
            
        except Exception as e:
            errors = state.get("errors") or []
            errors.append(f"Save results error: {str(e)}")
            state["errors"] = errors
            return state

    async def _load_memory_node(
        self, 
        state: DailyCheckState
    ) -> DailyCheckState:
        """Load relevant memory context"""
        # Placeholder for memory loading
        return state

    async def _biometric_analysis_node(
        self, 
        state: DailyCheckState
    ) -> DailyCheckState:
        """Analyze biometric data"""
        try:
            checkin_data = state.get("checkin_data", {})
            
            # Biometric agent analyzes readiness
            readiness = await self.biometric_agent.analyze({
                "sleep_quality": checkin_data.get("sleep_quality", 3),
                "energy_level": checkin_data.get("energy_level", "medium"),
                "soreness": checkin_data.get("soreness_level", "low")
            })
            
            state["readiness_score"] = readiness.get("score", 0.7)
            state["biometric_analysis"] = readiness
            
            return state
            
        except Exception as e:
            errors = state.get("errors") or []
            errors.append(f"Biometric analysis error: {str(e)}")
            state["errors"] = errors
            return state

    async def _occupation_analysis_node(
        self, 
        state: DailyCheckState
    ) -> DailyCheckState:
        """Analyze occupation impact"""
        try:
            user_profile = state.get("_user_profile", {})
            
            # Occupation agent analyzes work impact
            impact = await self.occupation_agent.analyze({
                "occupation": user_profile.get("occupation"),
                "work_hours": user_profile.get("work_hours", 8),
                "stress_level": state.get("checkin_data", {}).get("stress_level", "medium")
            })
            
            state["occupation_impact"] = impact
            
            return state
            
        except Exception as e:
            errors = state.get("errors") or []
            errors.append(f"Occupation analysis error: {str(e)}")
            state["errors"] = errors
            return state

    async def _emotional_analysis_node(
        self, 
        state: DailyCheckState
    ) -> DailyCheckState:
        """Analyze emotional state"""
        try:
            # Skip if no emotional data
            if not state.get("checkin_data", {}).get("mood"):
                return state
                
            result = await self.emotional_agent.analyze({
                "mood": state["checkin_data"].get("mood"),
                "stress_level": state["checkin_data"].get("stress_level"),
                "energy_level": state["checkin_data"].get("energy_level"),
                "user_message": state["checkin_data"].get("notes")
            })
            
            state["emotional_analysis"] = result
            return state
            
        except Exception as e:
            errors = state.get("errors") or []
            errors.append(f"Emotional analysis error: {str(e)}")
            state["errors"] = errors
            return state

    async def _holistic_analysis_node(
        self,
        state: DailyCheckState
    ) -> DailyCheckState:
        """Analyze holistic health and detect cross-dimension impacts"""
        try:
            user_profile = state.get("_user_profile", {})
            primary_goal = user_profile.get("primary_goal", "wellness")
            
            result = await self.holistic_agent.analyze({
                "primary_goal": primary_goal,
                "biometrics": {
                    "sleep_quality": state.get("checkin_data", {}).get("sleep_quality"),
                    "sleep_hours": state.get("checkin_data", {}).get("sleep_hours"),
                    "stress_level": state.get("checkin_data", {}).get("stress_level"),
                    "energy_level": state.get("checkin_data", {}).get("energy_level"),
                    "soreness_level": state.get("checkin_data", {}).get("soreness_level"),
                    "readiness_score": state.get("readiness_score")
                }
            })
            
            state["holistic_analysis"] = result
            
            # Check for focus shift recommendation
            shift = result.get("focus_shift_recommendation", {})
            if shift.get("should_shift"):
                # Override primary goal temporarily for this generation cycle
                # We don't change the user's DB profile, just the context for today's plan
                state["_temp_focus_shift"] = shift.get("target_focus")
                state["_focus_shift_reason"] = shift.get("reason")
            
            return state
            
        except Exception as e:
            errors = state.get("errors") or []
            errors.append(f"Holistic analysis error: {str(e)}")
            state["errors"] = errors
            return state

    async def _intervention_detection_node(
        self, 
        state: DailyCheckState
    ) -> DailyCheckState:
        """Detect if interventions are needed based on user state"""
        try:
            interventions = []
            checkin_data = state.get("checkin_data", {})
            emotional_analysis = state.get("emotional_analysis", {})
            
            # Check for poor sleep
            sleep_quality = checkin_data.get("sleep_quality")
            if sleep_quality and sleep_quality < 3:
                sleep_intervention = await self.sleep_agent.analyze({
                    "sleep_quality": sleep_quality,
                    "energy_level": checkin_data.get("energy_level"),
                    "user_profile": state.get("_user_profile", {})
                })
                interventions.append({
                    "type": "sleep",
                    "severity": "high" if sleep_quality < 2 else "medium",
                    "recommendation": sleep_intervention.get("recommendation", "Focus on sleep quality tonight"),
                    "actions": sleep_intervention.get("actions", [])
                })
            
            # Check for high stress
            stress_level = checkin_data.get("stress_level")
            if stress_level and stress_level in ["high", "very_high"]:
                stress_intervention = await self.stress_agent.analyze({
                    "stress_level": stress_level,
                    "emotional_state": emotional_analysis,
                    "occupation": state.get("_user_profile", {}).get("occupation")
                })
                interventions.append({
                    "type": "stress",
                    "severity": "high" if stress_level == "very_high" else "medium",
                    "recommendation": stress_intervention.get("recommendation", "Consider stress management techniques"),
                    "actions": stress_intervention.get("actions", [])
                })
            
            # Check for high soreness (potential injury)
            soreness_level = checkin_data.get("soreness_level")
            if soreness_level and soreness_level in ["high", "severe"]:
                interventions.append({
                    "type": "recovery",
                    "severity": "high" if soreness_level == "severe" else "medium",
                    "recommendation": "Reduce workout intensity today",
                    "actions": ["Active recovery", "Stretching", "Light cardio only"]
                })
            
            state["active_interventions"] = interventions
            
            return state
            
        except Exception as e:
            errors = state.get("errors") or []
            errors.append(f"Intervention detection error: {str(e)}")
            state["errors"] = errors
            return state

    async def _barrier_detection_node(
        self, 
        state: DailyCheckState
    ) -> DailyCheckState:
        """Detect potential barriers to compliance"""
        try:
            # Barrier agent analyzes potential obstacles
            barriers = await self.barrier_agent.analyze({
                "schedule": state.get("calendar_events", []),
                "energy": state.get("checkin_data", {}).get("energy_level"),
                "stress": state.get("checkin_data", {}).get("stress_level")
            })
            
            if barriers.get("detected", False):
                # Add barrier mitigation to interventions
                interventions = state.get("active_interventions", [])
                interventions.append({
                    "type": "barrier",
                    "severity": "medium",
                    "recommendation": f"Potential barrier detected: {barriers.get('primary_barrier')}",
                    "actions": barriers.get("mitigation_strategies", [])
                })
                state["active_interventions"] = interventions
            
            return state
            
        except Exception as e:
            errors = state.get("errors") or []
            errors.append(f"Barrier detection error: {str(e)}")
            state["errors"] = errors
            return state

    async def _schedule_check_node(
        self, 
        state: DailyCheckState
    ) -> DailyCheckState:
        """Check calendar for conflicts"""
        try:
            calendar_events = state.get("calendar_events", [])
            
            # Calendar agent identifies conflicts
            conflicts = await self.calendar_agent.analyze({
                "calendar_events": calendar_events,
                "current_date": state["current_date"]
            })
            
            state["schedule_conflicts"] = conflicts.get("conflicts", [])
            
            return state
            
        except Exception as e:
            errors = state.get("errors") or []
            errors.append(f"Schedule check error: {str(e)}")
            state["errors"] = errors
            return state
    
    
    async def _workout_generation_node(
        self, 
        state: DailyCheckState
    ) -> DailyCheckState:
        """
        Generate personalized daily plan based on user's primary goal.
        
        NEW: Routes to goal-specific plan generators instead of generic workout generation.
        """
        try:
            user_profile = state.get("_user_profile", {})
            
            # Determine effective goal for today
            # If Holistic Agent recommended a shift (e.g., "sleep" due to exhaustion), use that
            effective_goal = state.get("_temp_focus_shift") or user_profile.get("primary_goal", "wellness")
            
            # Get the appropriate plan generator
            plan_generator = get_plan_generator(effective_goal)
            
            # Generate personalized daily plan
            daily_plan = await plan_generator.generate(
                user_profile=user_profile,
                biometrics={
                    "readiness_score": state.get("readiness_score", 0.7),
                    "sleep_quality": state.get("checkin_data", {}).get("sleep_quality", 3),
                    "sleep_hours": state.get("checkin_data", {}).get("sleep_hours", 7),
                    "energy_level": state.get("checkin_data", {}).get("energy_level", "medium"),
                    "stress_level": state.get("checkin_data", {}).get("stress_level", "low"),
                    "soreness_level": state.get("checkin_data", {}).get("soreness_level", "low")
                },
                context={
                    "interventions": state.get("active_interventions", []),
                    "barriers": state.get("barriers", []),
                    "schedule": state.get("calendar_events", []),
                    "focus_shift_reason": state.get("_focus_shift_reason")  # Pass reason if shifted
                }
            )
            
            # Add focus shift notice to morning briefing if applicable
            if state.get("_temp_focus_shift"):
                reason = state.get("_focus_shift_reason", "health balance")
                notice = f"\n\n⚠️ FOCUS SHIFT: Today's plan is shifted to {effective_goal.upper()} focus due to {reason}. Your primary goal will resume once you recover."
                daily_plan["morning_briefing"] += notice
            
            # Store the complete daily plan
            state["daily_plan"] = daily_plan
            state["morning_briefing"] = daily_plan.get("morning_briefing", "")
            state["daily_tasks"] = daily_plan.get("tasks", [])
            
            # For backwards compatibility, also store workout_plan if it exists
            if "workout" in daily_plan.get("primary_focus", {}):
                state["workout_plan"] = daily_plan["primary_focus"]["workout"]
            
            return state
            
        except Exception as e:
            errors = state.get("errors") or []
            errors.append(f"Daily plan generation error: {str(e)}")
            state["errors"] = errors
            return state

    async def _workout_modification_node(
        self, 
        state: DailyCheckState
    ) -> DailyCheckState:
        """Modify workout based on interventions"""
        try:
            interventions = state.get("active_interventions", [])
            workout_plan = state.get("workout_plan", {})
            
            if interventions and workout_plan:
                # Modify workout if needed
                modified = await self.workout_mod_agent.analyze({
                    "original_workout": workout_plan,
                    "interventions": interventions,
                    "readiness": state.get("readiness_score")
                })
                
                state["workout_plan"] = modified.get("workout", workout_plan)
                state["modifications"] = modified.get("modifications", [])
            
            return state
            
        except Exception as e:
            errors = state.get("errors") or []
            errors.append(f"Workout modification error: {str(e)}")
            state["errors"] = errors
            return state

    async def _task_generation_node(
        self, 
        state: DailyCheckState
    ) -> DailyCheckState:
        """Generate daily tasks"""
        try:
            # Task agent generates tasks
            tasks = await self.task_agent.analyze({
                "workout": state.get("workout_plan"),
                "interventions": state.get("active_interventions"),
                "occupation": state.get("occupation_impact")
            })
            
            state["daily_tasks"] = tasks.get("tasks", [])
            
            return state
            
        except Exception as e:
            errors = state.get("errors") or []
            errors.append(f"Task generation error: {str(e)}")
            state["errors"] = errors
            return state

    async def _save_results_node(
        self, 
        state: DailyCheckState,
        db: AsyncSession
    ) -> DailyCheckState:
        """Save generated plan to database"""
        # This would be implemented to save to DB
        # For now just return state
        return state

    async def run(
        self, 
        initial_state: Dict[str, Any],
        db: AsyncSession
    ) -> DailyCheckState:
        """Execute the workflow"""
        # Inject db into nodes that need it
        async def fetch_with_db(state):
            return await self._fetch_user_context(state, db)
        
        async def save_results_with_db(state):
            return await self._save_results_node(state, db)
        
        # Re-build the graph with db-aware nodes
        workflow = StateGraph(DailyCheckState)
        
        # Add nodes
        workflow.add_node("fetch_profile", fetch_with_db)
        workflow.add_node("load_memory", self._load_memory_node)
        workflow.add_node("analyze_biometrics", self._biometric_analysis_node)
        workflow.add_node("analyze_occupation", self._occupation_analysis_node)
        workflow.add_node("analyze_emotions", self._emotional_analysis_node)
        workflow.add_node("detect_interventions", self._intervention_detection_node)
        workflow.add_node("detect_barriers", self._barrier_detection_node)
        workflow.add_node("check_schedule", self._schedule_check_node)
        workflow.add_node("generate_workout", self._workout_generation_node)
        workflow.add_node("modify_workout", self._workout_modification_node)
        workflow.add_node("generate_tasks", self._task_generation_node)
        workflow.add_node("save_results", save_results_with_db)
        
        # Define flow
        workflow.set_entry_point("fetch_profile")
        workflow.add_edge("fetch_profile", "load_memory")
        workflow.add_edge("load_memory", "analyze_biometrics")
        workflow.add_edge("analyze_biometrics", "analyze_occupation")
        workflow.add_edge("analyze_occupation", "analyze_emotions")
        workflow.add_edge("analyze_emotions", "detect_interventions")
        workflow.add_edge("detect_interventions", "detect_barriers")
        workflow.add_edge("detect_barriers", "check_schedule")
        workflow.add_edge("check_schedule", "generate_workout")
        workflow.add_edge("generate_workout", "modify_workout")
        workflow.add_edge("modify_workout", "generate_tasks")
        workflow.add_edge("generate_tasks", "save_results")
        workflow.add_edge("save_results", END)
        
        graph = workflow.compile()
        
        # Run the graph
        result = await graph.ainvoke(initial_state)
        return result
