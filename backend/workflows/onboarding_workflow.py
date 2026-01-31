"""
Onboarding Workflow - Coordinates agents for initial goal setting
"""
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from workflows.state import OnboardingState
from agents.resolution_tracking.goal_setting_agent import GoalSettingAgent
from agents.resolution_tracking.failure_pattern_agent import FailurePatternAgent
from agents.meta_coordinator import MetaCoordinator
from services.user_service import UserService
from memory.agent_memory import AgentMemory
from sqlalchemy.ext.asyncio import AsyncSession


class OnboardingWorkflow:
    """Orchestrates the onboarding multi-agent debate"""
    
    def __init__(self):
        self.goal_agent = GoalSettingAgent()
        self.failure_agent = FailurePatternAgent()
        self.coordinator = MetaCoordinator()
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(OnboardingState)
        
        # Add nodes
        workflow.add_node("fetch_profile", self._fetch_user_profile)
        workflow.add_node("load_memory", self._load_memory_node)
        workflow.add_node("goal_setting", self._goal_setting_node)
        workflow.add_node("failure_analysis", self._failure_analysis_node)
        workflow.add_node("coordinate", self._coordination_node)
        workflow.add_node("persist_memory", self._persist_memory_node)
        
        # Define flow
        workflow.set_entry_point("fetch_profile")
        workflow.add_edge("fetch_profile", "load_memory")
        workflow.add_edge("load_memory", "goal_setting")
        workflow.add_edge("goal_setting", "failure_analysis")
        workflow.add_edge("failure_analysis", "coordinate")
        workflow.add_edge("coordinate", "persist_memory")
        workflow.add_edge("persist_memory", END)
        
        return workflow.compile()
    
    async def _fetch_user_profile(
        self, 
        state: OnboardingState,
        db: AsyncSession
    ) -> OnboardingState:
        """Fetch and cache user profile"""
        user_profile = await UserService.get_user_profile(
            int(state["user_id"]), 
            db
        )
        state["_user_profile"] = user_profile
        return state
    
    async def _load_memory_node(
        self,
        state: OnboardingState,
        db: AsyncSession
    ) -> OnboardingState:
        """Load user memories from database into state"""
        memory_data = await AgentMemory.load_to_state(
            user_id=int(state["user_id"]),
            db=db,
            state_type="onboarding"
        )
        state["user_memory"] = memory_data
        state["memory_updates"] = []  # Initialize for agents to add learnings
        return state
    
    async def _goal_setting_node(
        self, 
        state: OnboardingState
    ) -> OnboardingState:
        """Goal Setting Agent proposes plan"""
        result = await self.goal_agent.analyze({
            "resolution_text": state["resolution_text"],
            "life_constraints": state.get("life_constraints", []),
            "_user_profile": state.get("_user_profile", {})
        })
        
        state["goal_analysis"] = result["goal_analysis"]
        return state
    
    async def _failure_analysis_node(
        self, 
        state: OnboardingState
    ) -> OnboardingState:
        """Failure Pattern Agent analyzes and challenges"""
        # Analyze failure patterns
        result = await self.failure_agent.analyze({
            "past_attempts": state.get("past_attempts", ""),
            "goal_analysis": state["goal_analysis"]
        })
        state["failure_risk"] = result["failure_risk"]
        
        # Challenge the plan
        challenge = await self.failure_agent.challenge(
            proposed_plan=state["goal_analysis"],
            challenger_context={"past_attempts": state.get("past_attempts", "")}
        )
        state["failure_agent_challenge"] = challenge
        
        return state
    
    async def _coordination_node(
        self, 
        state: OnboardingState
    ) -> OnboardingState:
        """Meta-Coordinator synthesizes debate"""

        # Build debate history 
        goal_analysis = state.get("goal_analysis", {})
        failure_risk = state.get("failure_risk", {})
        challenge = state.get("failure_agent_challenge", {})

        debate_history = [
            {
            "agent": "Goal Setting Agent",
            "role": "Proposes ambitious plan",

            "proposal": {
                "interpreted_goal": goal_analysis.get("interpreted_goal"),
                "weekly_target": goal_analysis.get("weekly_target"),
                "first_milestone": goal_analysis.get("first_milestone"),
                "reasoning": goal_analysis.get("reasoning")
            }

            },

            {
            "agent": "Failure Pattern Agent",
            "role": "Challenges and identifies risks",
            "analysis": {
                "identified_patterns": failure_risk.get("identified_patterns", []),
                "quit_probability": failure_risk.get("quit_probability"),
                "plan_concerns": failure_risk.get("plan_concerns", [])
            },
            "challenge": {
                "stance": challenge.get("stance"),
                "reasoning": challenge.get("reasoning"),
                "counter_proposal": challenge.get("counter_proposal")
            }
            }
        ]
        
        
        
        # Extract primary goal from state (passed from API)
        primary_goal = state.get("primary_goal", "wellness")
        
        synthesis = await self.coordinator.synthesize_debate(debate_history, primary_goal)
        
        state["final_plan"] = synthesis.get("final_decision", {})
        
        # Inject the raw debate history so the frontend can visualize it
        summary = synthesis.get("debate_summary", {})
        summary["agents"] = debate_history
        summary["synthesis"] = synthesis.get("debate_summary", {}).get("synthesis_rationale", "")
        state["debate_summary"] = summary
        
        state["safety_adjustments"] = synthesis.get("safety_adjustments", [])
        state["confidence_score"] = synthesis.get("confidence", 0.0)
        
        return state
    
    async def _persist_memory_node(
        self,
        state: OnboardingState,
        db: AsyncSession
    ) -> OnboardingState:
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
    ) -> OnboardingState:
        """Execute the workflow"""
        # Inject db into nodes that need it
        async def fetch_with_db(state):
            return await self._fetch_user_profile(state, db)
        
        async def load_memory_with_db(state):
            return await self._load_memory_node(state, db)
        
        async def persist_memory_with_db(state):
            return await self._persist_memory_node(state, db)
        
        # Update the graph with db-aware nodes
        workflow = StateGraph(OnboardingState)
        workflow.add_node("fetch_profile", fetch_with_db)
        workflow.add_node("load_memory", load_memory_with_db)
        workflow.add_node("goal_setting", self._goal_setting_node)
        workflow.add_node("failure_analysis", self._failure_analysis_node)
        workflow.add_node("coordinate", self._coordination_node)
        workflow.add_node("persist_memory", persist_memory_with_db)
        
        workflow.set_entry_point("fetch_profile")
        workflow.add_edge("fetch_profile", "load_memory")
        workflow.add_edge("load_memory", "goal_setting")
        workflow.add_edge("goal_setting", "failure_analysis")
        workflow.add_edge("failure_analysis", "coordinate")
        workflow.add_edge("coordinate", "persist_memory")
        workflow.add_edge("persist_memory", END)
        
        graph = workflow.compile()
        
        # Run the graph
        result = await graph.ainvoke(initial_state)
        return result
