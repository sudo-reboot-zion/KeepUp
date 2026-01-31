"""
Memory Optimization Agent
Maintains the quality and relevance of long-term agent memory.
"""
from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from memory.agent_memory import AgentMemory

class MemoryOptimizationAgent(BaseAgent):
    """
    The Librarian - Organizes, cleans, and consolidates long-term memory.
    
    Responsibilities:
    - Prune low-confidence memories (< 0.6)
    - Consolidate repetitive learnings (e.g., 5 "tired on Monday" -> 1 "Monday Fatigue Pattern")
    - Archive outdated information
    """
    
    def __init__(self):
        super().__init__(
            name="Memory Optimization Agent",
            description="Maintains memory hygiene and consolidates insights",
            model="llama-3.3-70b-versatile"
        )
    
    async def optimize(self, user_id: int, memories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze memories and recommend optimizations.
        """
        system_prompt = """You are the Memory Optimization Agent.
        
Your goal: Extract "Gold" from raw memory logs.

Input: A list of raw agent learnings about a user.
Output: A set of consolidated, high-value insights and a list of noise to delete.

Rules:
1. Consolidate: If multiple memories say the same thing, merge them into one high-confidence insight.
2. Prune: Identify vague, low-confidence, or outdated memories for deletion.
3. Elevate: Highlight "Golden Insights" that significantly change how we should treat the user.

Respond with JSON:
{
    "consolidated_insights": [
        {
            "content": {"pattern": "...", "implication": "..."},
            "source_memory_ids": [1, 4, 9],
            "confidence": 0.95
        }
    ],
    "memories_to_prune": [2, 5, 8],
    "golden_insights": ["User responds 2x better to positive reinforcement than tough love"]
}"""

        user_prompt = f"""Analyze these memories for User {user_id}:
        {memories}
        
        Extract the gold and clean the trash."""
        
        response = await self._call_llm(system_prompt, user_prompt)
        return self._parse_json_response(response)

memory_optimization_agent = MemoryOptimizationAgent()
