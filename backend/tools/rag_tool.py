"""
RAG Tool - Clean interface for agents to query knowledge
Wraps the RAG retriever with a simple, agent-friendly API
"""
from typing import Dict, Any, Optional
from memory.rag.retriever import rag_retriever


class RAGTool:
    """
    Tool that agents use to query the knowledge base.
    Handles all the complexity of RAG + Tavily fallback.
    """
    
    def __init__(self):
        self.retriever = rag_retriever
        self.name = "rag_search"
        self.description = """Search the fitness knowledge base for scientific information 
        about training, nutrition, recovery, injury prevention, and habit psychology. 
        Automatically searches the web if knowledge base doesn't have the answer."""
    
    async def search(
        self,
        query: str,
        category: Optional[str] = None,
        k: int = 3
    ) -> Dict[str, Any]:
        """
        Search for knowledge relevant to the query.
        
        Args:
            query: What to search for (e.g. "HIIT workout guidelines", "protein timing")
            category: Optional filter ("fitness", "nutrition", "recovery", "resolution_psychology")
            k: Number of results to return
            
        Returns:
            Dict with:
                - success: bool
                - context: str (formatted context ready for LLM prompt)
                - sources: List[str] (where info came from)
                - used_web_search: bool (True if Tavily was used)
        """
        try:
            # Ensure RAG is initialized
            if not self.retriever.is_initialized:
                await self.retriever.initialize()
            
            # Get results (RAG + Tavily fallback)
            results = await self.retriever.retrieve(
                query=query,
                category=category,
                k=k,
                use_tavily_fallback=True
            )
            
            if not results:
                return {
                    "success": False,
                    "context": "No relevant information found.",
                    "sources": [],
                    "used_web_search": False,
                    "error": "No results found"
                }
            
            # Format context for LLM
            context = await self.retriever.retrieve_with_context(
                query=query,
                category=category,
                k=k,
                use_tavily_fallback=True
            )
            
            # Extract sources
            sources = [r['metadata'].get('source', 'unknown') for r in results]
            
            # Check if web search was used
            used_web = any(r['metadata'].get('from_tavily', False) for r in results)
            
            return {
                "success": True,
                "context": context,
                "sources": sources,
                "used_web_search": used_web,
                "num_results": len(results)
            }
            
        except Exception as e:
            return {
                "success": False,
                "context": "",
                "sources": [],
                "used_web_search": False,
                "error": str(e)
            }
    
    # Domain-specific search helpers
    async def search_fitness(self, query: str, k: int = 3) -> Dict[str, Any]:
        """Search fitness-specific knowledge"""
        return await self.search(query, category="fitness", k=k)
    
    async def search_nutrition(self, query: str, k: int = 3) -> Dict[str, Any]:
        """Search nutrition-specific knowledge"""
        return await self.search(query, category="nutrition", k=k)
    
    async def search_recovery(self, query: str, k: int = 3) -> Dict[str, Any]:
        """Search recovery-specific knowledge"""
        return await self.search(query, category="recovery", k=k)
    
    async def search_psychology(self, query: str, k: int = 3) -> Dict[str, Any]:
        """Search habit psychology knowledge"""
        return await self.search(query, category="resolution_psychology", k=k)
    
    def format_for_prompt(self, search_result: Dict[str, Any]) -> str:
        """
        Format search result for inclusion in agent prompt.
        
        Usage in agent:
            knowledge = await rag_tool.search("protein timing")
            context = rag_tool.format_for_prompt(knowledge)
            prompt = f"Given this knowledge:\n{context}\n\nAnswer: {user_question}"
        """
        if not search_result.get("success"):
            return "No relevant knowledge available."
        
        context = search_result.get("context", "")
        sources = search_result.get("sources", [])
        
        footer = "\n\n---\nSources:\n" + "\n".join(f"- {s}" for s in sources[:3])
        
        return context + footer


# Singleton instance
rag_tool = RAGTool()