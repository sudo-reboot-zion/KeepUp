"""
Intervention Workflow - Triggers when user is at risk of quitting
This is where the AI becomes PROACTIVE instead of reactive
"""
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from workflows.state import InterventionState
from agents.contextual_awareness.barrier_detection_agent import BarrierDetectionAgent
from agents.contextual_awareness.motivation_agent import MotivationAgent
from agents.adaptive_intervention.workout_modification_agent import workout_modification_agent
from agents.mental_wellness.stress_management_agent import StressManagementAgent
from agents.meta_coordinator import MetaCoordinator
from services.user_service import UserService
from memory.agent_memory import AgentMemory
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime


class InterventionWorkflow:
    """
    Autonomous intervention system that:
    1. Detects WHY user is struggling
    2. Generates multiple intervention options
    3. AUTONOMOUSLY applies protective changes
    4. Explains reasoning transparently
    
    This is the "competitor killer" feature - AI that acts, not just advises
    """
    
    def __init__(self):
        self.barrier_agent = BarrierDetectionAgent()
        self.motivation_agent = MotivationAgent()
        self.workout_agent = workout_modification_agent
        self.stress_agent = StressManagementAgent()
        self.coordinator = MetaCoordinator()
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build intervention graph"""
        workflow = StateGraph(InterventionState)
        
        # Add nodes
        workflow.add_node("load_memory", self._load_memory_node)
        workflow.add_node("detect_barriers", self._detect_barriers_node)
        workflow.add_node("assess_motivation", self._assess_motivation_node)
        workflow.add_node("generate_options", self._generate_options_node)
        workflow.add_node("autonomous_action", self._autonomous_action_node)
        workflow.add_node("finalize", self._finalize_node)
        workflow.add_node("persist_memory", self._persist_memory_node)
        
        # Define flow
        workflow.set_entry_point("load_memory")
        workflow.add_edge("load_memory", "detect_barriers")
        workflow.add_edge("detect_barriers", "assess_motivation")
        workflow.add_edge("assess_motivation", "generate_options")
        workflow.add_edge("generate_options", "autonomous_action")
        workflow.add_edge("autonomous_action", "finalize")
        workflow.add_edge("finalize", "persist_memory")
        workflow.add_edge("persist_memory", END)
        
        return workflow.compile()
    
    async def _load_memory_node(
        self,
        state: InterventionState,
        db: AsyncSession
    ) -> InterventionState:
        """Load user memories from database into state"""
        memory_data = await AgentMemory.load_to_state(
            user_id=int(state["user_id"]),
            db=db,
            state_type="intervention"
        )
        state["user_memory"] = memory_data
        state["memory_updates"] = []  # Initialize for agents to add learnings
        return state
    
    async def _detect_barriers_node(
        self, 
        state: InterventionState
    ) -> InterventionState:
        """Detect WHAT is blocking the user"""
        try:
            # Build context
            context = {
                "missed_workouts": state.get("missed_workouts", 0),
                "days_inactive": state.get("days_inactive", 0),
                "current_week": state.get("current_week", 1),
                "historical_quit_week": state.get("historical_quit_week")
            }
            
            # Barrier Detection Agent identifies obstacles
            barriers = await self.barrier_agent.analyze(context)
            
            state["detected_barriers"] = barriers.get("barriers", [])
            state["barrier_categories"] = barriers.get("categories", [])
            
            return state
            
        except Exception as e:
            errors = state.get("errors") or []
            errors.append(f"Barrier detection error: {str(e)}")
            state["errors"] = errors
            return state
    
    async def _assess_motivation_node(
        self, 
        state: InterventionState
    ) -> InterventionState:
        """Assess psychological state"""
        try:
            context = {
                "days_inactive": state.get("days_inactive", 0),
                "detected_barriers": state.get("detected_barriers", []),
                "abandonment_probability": state.get("abandonment_probability", 0.0)
            }
            
            # Motivation Agent assesses psychological factors
            motivation = await self.motivation_agent.analyze(context)
            
            state["motivation_drop"] = motivation.get("motivation_drop", False)
            state["motivational_state"] = motivation.get("state", "unknown")
            
            return state
            
        except Exception as e:
            errors = state.get("errors") or []
            errors.append(f"Motivation assessment error: {str(e)}")
            state["errors"] = errors
            return state
    
    async def _generate_options_node(
        self, 
        state: InterventionState
    ) -> InterventionState:
        """Generate multiple intervention strategies"""
        try:
            barriers = state.get("detected_barriers", [])
            motivation_state = state.get("motivational_state", "unknown")
            
            # Generate options based on barriers
            options = []
            
            # Option 1: Reduce difficulty
            if "time_constraint" in state.get("barrier_categories", []):
                options.append({
                    "type": "reduce_difficulty",
                    "action": "Reduce workout duration by 40%",
                    "rationale": "Time barriers detected - make it easier to fit in schedule",
                    "autonomous": True
                })
            
            # Option 2: Change workout type
            if "monotony" in state.get("barrier_categories", []):
                options.append({
                    "type": "variety_injection",
                    "action": "Switch to different exercise modality",
                    "rationale": "Motivation drop likely due to boredom",
                    "autonomous": False
                })
            
            # Option 3: Add rest day
            if state.get("days_inactive", 0) == 0 and state.get("missed_workouts", 0) > 2:
                options.append({
                    "type": "mandatory_rest",
                    "action": "Force 2-day rest period",
                    "rationale": "User may be burned out - prevent injury",
                    "autonomous": True
                })
            
            # Option 4: Stress management intervention
            if "stress" in str(barriers).lower():
                stress_intervention = await self.stress_agent.analyze({
                    "barriers": barriers,
                    "motivation_state": motivation_state
                })
                options.append({
                    "type": "stress_management",
                    "action": stress_intervention.get("recommendation", ""),
                    "rationale": "High stress detected",
                    "autonomous": False
                })
            
            state["recommended_actions"] = options
            
            return state
            
        except Exception as e:
            errors = state.get("errors") or []
            errors.append(f"Option generation error: {str(e)}")
            state["errors"] = errors
            return state
    
    async def _autonomous_action_node(
        self, 
        state: InterventionState
    ) -> InterventionState:
        """
        AUTONOMOUS ACTION - AI takes protective measures WITHOUT asking
        This is what makes Euexia different from competitors
        """
        try:
            options = state.get("recommended_actions", [])
            
            # Filter for autonomous actions
            autonomous_actions = [o for o in options if o.get("autonomous", False)]
            
            actions_taken = []
            
            for action in autonomous_actions:
                action_type = action.get("type")
                
                if action_type == "reduce_difficulty":
                    # Autonomously modify next workout
                    # TODO: Actually modify user's plan in database
                    actions_taken.append({
                        "action": action.get("action"),
                        "rationale": action.get("rationale"),
                        "timestamp": datetime.utcnow().isoformat(),
                        "type": "protective_modification"
                    })
                
                elif action_type == "mandatory_rest":
                    # Block workouts for 2 days
                    # TODO: Update user's calendar in database
                    actions_taken.append({
                        "action": "Blocked workouts for 48 hours",
                        "rationale": "Preventing burnout and injury",
                        "timestamp": datetime.utcnow().isoformat(),
                        "type": "protective_block"
                    })
            
            state["autonomous_actions_taken"] = actions_taken
            
            # Non-autonomous actions become suggestions
            suggestions = [o for o in options if not o.get("autonomous", False)]
            state["alternative_plans"] = suggestions
            
            return state
            
        except Exception as e:
            errors = state.get("errors") or []
            errors.append(f"Autonomous action error: {str(e)}")
            state["errors"] = errors
            return state
    
    async def _finalize_node(
        self, 
        state: InterventionState
    ) -> InterventionState:
        """Package intervention results"""
        try:
            # Build intervention summary
            intervention_plan = {
                "triggered_at": datetime.utcnow().isoformat(),
                "detected_barriers": state.get("detected_barriers", []),
                "abandonment_probability": state.get("abandonment_probability", 0.0),
                "autonomous_actions": state.get("autonomous_actions_taken", []),
                "user_suggestions": state.get("alternative_plans", []),
                "expected_impact": self._estimate_impact(state)
            }
            
            state["intervention_plan"] = intervention_plan
            state["timestamp"] = datetime.utcnow().isoformat()
            
            return state
            
        except Exception as e:
            errors = state.get("errors") or []
            errors.append(f"Finalization error: {str(e)}")
            state["errors"] = errors
            return state
    
    def _estimate_impact(self, state: InterventionState) -> Dict[str, Any]:
        """Estimate expected impact of interventions"""
        actions = state.get("autonomous_actions_taken", [])
        current_prob = state.get("abandonment_probability", 0.7)
        
        # Simple heuristic - each action reduces quit probability
        reduction = len(actions) * 0.15
        new_prob = max(0.1, current_prob - reduction)
        
        return {
            "abandonment_probability_before": current_prob,
            "abandonment_probability_after": new_prob,
            "expected_reduction": reduction,
            "confidence": 0.7
        }
    
    async def _persist_memory_node(
        self,
        state: InterventionState,
        db: AsyncSession
    ) -> InterventionState:
        """Persist memory updates from state to database"""
        await AgentMemory.persist_from_state(
            user_id=int(state["user_id"]),
            db=db,
            memory_updates=state.get("memory_updates", [])
        )
        return state
    
    async def run(
        self, 
        initial_state: Dict[str, Any],
        db: AsyncSession
    ) -> InterventionState:
        """Execute intervention workflow"""
        
        # Inject db into nodes that need it
        async def load_memory_with_db(state):
            return await self._load_memory_node(state, db)
        
        async def persist_memory_with_db(state):
            return await self._persist_memory_node(state, db)
        
        # Rebuild graph with db-aware nodes
        workflow = StateGraph(InterventionState)
        workflow.add_node("load_memory", load_memory_with_db)
        workflow.add_node("detect_barriers", self._detect_barriers_node)
        workflow.add_node("assess_motivation", self._assess_motivation_node)
        workflow.add_node("generate_options", self._generate_options_node)
        workflow.add_node("autonomous_action", self._autonomous_action_node)
        workflow.add_node("finalize", self._finalize_node)
        workflow.add_node("persist_memory", persist_memory_with_db)
        
        workflow.set_entry_point("load_memory")
        workflow.add_edge("load_memory", "detect_barriers")
        workflow.add_edge("detect_barriers", "assess_motivation")
        workflow.add_edge("assess_motivation", "generate_options")
        workflow.add_edge("generate_options", "autonomous_action")
        workflow.add_edge("autonomous_action", "finalize")
        workflow.add_edge("finalize", "persist_memory")
        workflow.add_edge("persist_memory", END)
        
        graph = workflow.compile()
        
        # Run the graph
        result = await graph.ainvoke(initial_state)
        return result