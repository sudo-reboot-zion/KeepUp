"""
Resolution Workflow - Weekly check-in and progress evaluation
Detects if user is falling behind and triggers interventions proactively
"""
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from workflows.state import DailyCheckState
from agents.resolution_tracking.progress_tracking_agent import ProgressTrackingAgent
from agents.resolution_tracking.failure_pattern_agent import FailurePatternAgent
from agents.meta_coordinator import MetaCoordinator
from services.user_service import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta


class ResolutionWorkflow:
    """
    Weekly check-in workflow that:
    1. Evaluates progress vs. plan
    2. Detects early warning signs of abandonment
    3. Adjusts difficulty up/down
    4. Triggers intervention workflow if needed
    """
    
    def __init__(self):
        self.progress_agent = ProgressTrackingAgent()
        self.failure_agent = FailurePatternAgent()
        self.coordinator = MetaCoordinator()
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build LangGraph workflow"""
        from typing import TypedDict
        
        # Define state for this workflow
        class ResolutionCheckState(TypedDict):
            user_id: str
            current_week: int
            workouts_completed_this_week: int
            workouts_target_this_week: int
            adherence_rate: float
            skip_pattern: list
            progress_analysis: dict
            risk_assessment: dict
            needs_intervention: bool
            adjustment_recommendations: dict
            final_decision: dict
            errors: list
        
        workflow = StateGraph(ResolutionCheckState)
        
        # Add nodes
        workflow.add_node("fetch_data", self._fetch_progress_data)
        workflow.add_node("analyze_progress", self._analyze_progress_node)
        workflow.add_node("detect_risks", self._detect_risk_node)
        workflow.add_node("decide_action", self._decide_action_node)
        
        # Define flow
        workflow.set_entry_point("fetch_data")
        workflow.add_edge("fetch_data", "analyze_progress")
        workflow.add_edge("analyze_progress", "detect_risks")
        workflow.add_edge("detect_risks", "decide_action")
        workflow.add_edge("decide_action", END)
        
        return workflow.compile()
    
    async def _fetch_progress_data(
        self, 
        state: Dict[str, Any],
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Fetch user's progress data for the week"""
        try:
            user_id = int(state["user_id"])
            
            # Get user profile and resolution
            user_profile = await UserService.get_user_profile(user_id, db)
            resolution = user_profile.get("resolution", {})
            
            # Get workout history (last 7 days)
            # TODO: Implement UserService.get_workout_history
            # For now, mock data
            workouts_this_week = state.get("workouts_completed_this_week", 0)
            target = resolution.get("weekly_target", "3x/week")
            
            # Parse target (e.g., "3x/week" -> 3)
            target_num = int(target.split("x")[0]) if "x" in target else 3
            
            # Calculate adherence
            adherence_rate = workouts_this_week / target_num if target_num > 0 else 0.0
            
            # Get skip pattern (last 14 days)
            # TODO: Fetch from database
            # Format: [True, False, True, True, False, False, True, ...]
            # True = workout done, False = skipped
            skip_pattern = state.get("skip_pattern", [])
            
            state["workouts_target_this_week"] = target_num
            state["adherence_rate"] = adherence_rate
            state["_user_profile"] = user_profile
            state["_resolution"] = resolution
            
            # Load user memory
            from memory.agent_memory import AgentMemory
            user_memory = await AgentMemory.load_to_state(
                user_id=user_id,
                db=db,
                state_type="resolution_check"
            )
            state["user_memory"] = user_memory
            
            return state
            
        except Exception as e:
            errors = state.get("errors") or []
            errors.append(f"Data fetch error: {str(e)}")
            state["errors"] = errors
            return state
    
    async def _analyze_progress_node(
        self, 
        state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Progress Tracking Agent analyzes adherence"""
        try:
            analysis = await self.progress_agent.analyze({
                "current_week": state.get("current_week", 1),
                "workouts_completed": state.get("workouts_completed_this_week", 0),
                "workouts_target": state.get("workouts_target_this_week", 3),
                "adherence_rate": state.get("adherence_rate", 0.0),
                "skip_pattern": state.get("skip_pattern", []),
                "skip_pattern": state.get("skip_pattern", []),
                "user_profile": state.get("_user_profile", {}),
                "user_memory": state.get("user_memory", {})
            })
            
            state["progress_analysis"] = analysis.get("analysis", {})
            
            return state
            
        except Exception as e:
            errors = state.get("errors") or []
            errors.append(f"Progress analysis error: {str(e)}")
            state["errors"] = errors
            return state
    
    async def _detect_risk_node(
        self, 
        state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Failure Pattern Agent detects abandonment risk"""
        try:
            progress = state.get("progress_analysis", {})
            
            # Build risk context
            risk_context = {
                "current_week": state.get("current_week", 1),
                "adherence_rate": state.get("adherence_rate", 0.0),
                "consecutive_skips": self._count_consecutive_skips(
                    state.get("skip_pattern", [])
                ),
                "progress_trend": progress.get("trend", "stable"),
                "user_profile": state.get("_user_profile", {})
            }
            
            # Failure agent assesses risk
            risk = await self.failure_agent.analyze({
                "past_attempts": state.get("_user_profile", {}).get("past_attempts", ""),
                "current_progress": progress,
                "risk_context": risk_context,
                "user_memory": state.get("user_memory", {})
            })
            
            state["risk_assessment"] = risk.get("failure_risk", {})
            
            # Determine if intervention needed
            quit_probability = risk.get("failure_risk", {}).get("quit_probability", 0.0)
            state["needs_intervention"] = quit_probability > 0.6
            
            return state
            
        except Exception as e:
            errors = state.get("errors") or []
            errors.append(f"Risk detection error: {str(e)}")
            state["errors"] = errors
            return state
    
    async def _decide_action_node(
        self, 
        state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Meta-Coordinator decides what to do"""
        try:
            progress = state.get("progress_analysis", {})
            risk = state.get("risk_assessment", {})
            
            # Build decision context
            debate_history = [
                {
                    "agent": "Progress Tracking Agent",
                    "analysis": progress
                },
                {
                    "agent": "Failure Pattern Agent",
                    "risk_assessment": risk,
                    "needs_intervention": state.get("needs_intervention", False)
                }
            ]
            
            # Coordinator makes decision
            decision = await self.coordinator.synthesize_debate(debate_history)
            
            state["adjustment_recommendations"] = decision.get("final_decision", {})
            state["final_decision"] = decision
            
            return state
            
        except Exception as e:
            errors = state.get("errors") or []
            errors.append(f"Decision error: {str(e)}")
            state["errors"] = errors
            return state
    
    def _count_consecutive_skips(self, skip_pattern: list) -> int:
        """Count how many days in a row were skipped"""
        if not skip_pattern:
            return 0
        
        consecutive = 0
        for completed in reversed(skip_pattern):
            if completed:
                break
            consecutive += 1
        
        return consecutive
    
    async def run(
        self, 
        initial_state: Dict[str, Any],
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Execute the workflow"""
        
        # Inject db into nodes that need it
        async def fetch_with_db(state):
            return await self._fetch_progress_data(state, db)
        
        # Rebuild graph with db-aware node
        from typing import TypedDict
        
        class ResolutionCheckState(TypedDict):
            user_id: str
            current_week: int
            workouts_completed_this_week: int
            workouts_target_this_week: int
            adherence_rate: float
            skip_pattern: list
            progress_analysis: dict
            risk_assessment: dict
            needs_intervention: bool
            adjustment_recommendations: dict
            final_decision: dict
            errors: list
        
        workflow = StateGraph(ResolutionCheckState)
        
        workflow.add_node("fetch_data", fetch_with_db)
        workflow.add_node("analyze_progress", self._analyze_progress_node)
        workflow.add_node("detect_risks", self._detect_risk_node)
        workflow.add_node("decide_action", self._decide_action_node)
        
        workflow.set_entry_point("fetch_data")
        workflow.add_edge("fetch_data", "analyze_progress")
        workflow.add_edge("analyze_progress", "detect_risks")
        workflow.add_edge("detect_risks", "decide_action")
        workflow.add_edge("decide_action", END)
        
        graph = workflow.compile()
        
        # Run the graph
        result = await graph.ainvoke(initial_state)
        return result