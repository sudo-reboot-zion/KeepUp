# tools/tavily_search_tool.py

"""
Tavily Search Tool - Web search for agents
"""
from typing import Dict, Any, List, Optional
from tavily import TavilyClient
from core.config import settings


class TavilySearchTool:
    """
    Tool for agents to search the web using Tavily API
    """
    
    def __init__(self):
        self.client = TavilyClient(api_key=settings.TAVILY_API_KEY)
        self.name = "tavily_search"
        self.description = """Search the web for current information, research papers, 
        fitness guidelines, nutrition data, or any factual information. 
        Use this when you need up-to-date knowledge beyond your training data."""
    
    async def search(
        self, 
        query: str, 
        search_depth: str = "basic",
        max_results: int = 5,
        include_domains: Optional[List[str]] = None,
        exclude_domains: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Search the web using Tavily
        
        Args:
            query: Search query
            search_depth: "basic" or "advanced"
            max_results: Number of results to return (1-10)
            include_domains: List of domains to prioritize
            exclude_domains: List of domains to exclude
            
        Returns:
            Dict with search results and sources
        """
        try:
            response = self.client.search(
                query=query,
                search_depth=search_depth,
                max_results=max_results,
                include_domains=include_domains,
                exclude_domains=exclude_domains,
                include_answer=True,  
                include_raw_content=False  
            )
            
            return {
                "success": True,
                "query": query,
                "answer": response.get("answer", ""),
                "results": [
                    {
                        "title": result.get("title"),
                        "url": result.get("url"),
                        "content": result.get("content"),
                        "score": result.get("score")
                    }
                    for result in response.get("results", [])
                ],
                "sources": [r.get("url") for r in response.get("results", [])]
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "query": query,
                "answer": "",
                "results": [],
                "sources": []
            }
    
    async def search_fitness_research(self, query: str) -> Dict[str, Any]:
        """Search specifically for fitness/health research"""
    
        trusted_domains = [
            "ncbi.nlm.nih.gov",
            "nih.gov",
            "mayoclinic.org",
            "health.harvard.edu",
            "acsm.org",  
            "nsca.com"   
        ]
        
        return await self.search(
            query=query,
            search_depth="advanced",
            max_results=5,
            include_domains=trusted_domains
        )
    
    async def search_nutrition_info(self, query: str) -> Dict[str, Any]:
        """Search specifically for nutrition information"""
        trusted_domains = [
            "nih.gov",
            "usda.gov",
            "nutrition.gov",
            "examine.com",
            "health.harvard.edu"
        ]
        
        return await self.search(
            query=query,
            search_depth="advanced",
            max_results=5,
            include_domains=trusted_domains
        )


# Singleton instance
tavily_tool = TavilySearchTool()