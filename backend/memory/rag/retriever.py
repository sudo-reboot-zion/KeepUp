"""
RAG Retriever - High-level interface for agents to query knowledge base
NOW WITH TAVILY FALLBACK - agents always get answers
"""
from typing import List, Dict, Any, Optional
from memory.rag.vector_store import vector_store
from memory.rag.document_loader import document_loader
from tools.tavily_search_tool import tavily_tool
from pathlib import Path


class RAGRetriever:
    """
    Hybrid retrieval system:
    1. Try RAG first (local knowledge base)
    2. If no good results → fallback to Tavily web search
    3. Cache Tavily results back into RAG for future queries
    """
    
    def __init__(self):
        self.vector_store = vector_store
        self.document_loader = document_loader
        self.tavily = tavily_tool
        self.knowledge_base_path = Path("memory/rag/knowledge_base")
        self.similarity_threshold = 0.7  # Minimum similarity to trust RAG result
        self.is_initialized = False
    
    async def initialize(self, force_rebuild: bool = False):
        """
        Initialize the RAG system.
        Load existing index or build new one from knowledge base.
        
        Args:
            force_rebuild: If True, rebuild index even if it exists
        """
        # Try to load existing index
        if not force_rebuild and self.vector_store.load("fitness_knowledge"):
            print("✅ RAG system ready (loaded from disk)")
            self.is_initialized = True
            return
        
        # Build new index from knowledge base
        print("🔨 Building RAG index from knowledge base...")
        
        if not self.knowledge_base_path.exists():
            print(f"⚠️  Knowledge base not found: {self.knowledge_base_path}")
            print("Creating directory. System will rely on Tavily for now.")
            self.knowledge_base_path.mkdir(parents=True, exist_ok=True)
            self.is_initialized = True
            return
        
        # Load and chunk all documents
        chunks, metadata = self.document_loader.load_and_chunk(
            self.knowledge_base_path,
            file_extensions=[".md", ".txt"]
        )
        
        if not chunks:
            print("⚠️  No documents found in knowledge base. Will use Tavily fallback.")
            self.is_initialized = True
            return
        
        # Add to vector store
        self.vector_store.add_documents(chunks, metadata)
        
        # Save for next time
        self.vector_store.save("fitness_knowledge")
        
        print("✅ RAG system ready (built from knowledge base)")
        self.is_initialized = True
    
    async def retrieve(
        self,
        query: str,
        category: Optional[str] = None,
        k: int = 3,
        use_tavily_fallback: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant knowledge for a query.
        Automatically falls back to Tavily if RAG results are poor.
        
        Args:
            query: What to search for
            category: Filter by category (fitness, nutrition, recovery, etc.)
            k: Number of results to return
            use_tavily_fallback: If True, use Tavily when RAG fails
            
        Returns:
            List of relevant document chunks with metadata
        """
        if not self.is_initialized:
            await self.initialize()
        
        # Try RAG first
        rag_results = self.vector_store.search(
            query=query,
            k=k,
            filter_category=category
        )
        
        # Check if RAG results are good enough
        if rag_results and self._are_results_good(rag_results):
            print(f"✅ RAG found {len(rag_results)} relevant results")
            return rag_results
        
        # RAG failed or returned poor results - fallback to Tavily
        if use_tavily_fallback:
            print(f"🌐 RAG results insufficient, searching web via Tavily...")
            return await self._search_with_tavily(query, category, k)
        
        return rag_results  # Return whatever RAG found, even if poor
    
    def _are_results_good(self, results: List[Dict[str, Any]]) -> bool:
        """Check if RAG results meet quality threshold"""
        if not results:
            return False
        
        # Check if at least one result has good similarity
        best_similarity = max(r.get("similarity", 0) for r in results)
        return best_similarity >= self.similarity_threshold
    
    async def _search_with_tavily(
        self, 
        query: str, 
        category: Optional[str], 
        k: int
    ) -> List[Dict[str, Any]]:
        """
        Search web using Tavily and format results like RAG results.
        Also caches results back into RAG for future queries.
        """
        # Choose search method based on category
        if category == "fitness":
            tavily_response = await self.tavily.search_fitness_research(query)
        elif category == "nutrition":
            tavily_response = await self.tavily.search_nutrition_info(query)
        else:
            tavily_response = await self.tavily.search(query, max_results=k)
        
        if not tavily_response.get("success"):
            print(f"❌ Tavily search failed: {tavily_response.get('error')}")
            return []
        
        # Format Tavily results to match RAG format
        formatted_results = []
        for result in tavily_response.get("results", [])[:k]:
            formatted_results.append({
                "document": result.get("content", ""),
                "metadata": {
                    "source": result.get("url", ""),
                    "title": result.get("title", ""),
                    "category": category or "web_search",
                    "from_tavily": True,
                    "score": result.get("score", 0)
                },
                "similarity": result.get("score", 0.5),  # Tavily score as similarity
                "distance": 1 - result.get("score", 0.5)
            })
        
        # Cache these results back into RAG for future queries
        if formatted_results:
            await self._cache_tavily_results(formatted_results, category)
        
        print(f"✅ Tavily found {len(formatted_results)} results")
        return formatted_results
    
    async def _cache_tavily_results(
        self, 
        results: List[Dict[str, Any]], 
        category: Optional[str]
    ):
        """
        Add Tavily results to RAG so we don't have to search again.
        This makes the system smarter over time.
        """
        try:
            for result in results:
                doc = result.get("document", "")
                meta = result.get("metadata", {})
                
                if doc and len(doc) > 50:  # Only cache substantial content
                    await self.add_knowledge(
                        text=doc,
                        metadata={
                            "category": category or "web_search",
                            "source": meta.get("source", "tavily"),
                            "title": meta.get("title", ""),
                            "cached_from_tavily": True
                        }
                    )
            print(f"💾 Cached {len(results)} Tavily results into RAG")
        except Exception as e:
            print(f"⚠️  Failed to cache Tavily results: {e}")
    
    async def retrieve_with_context(
        self,
        query: str,
        category: Optional[str] = None,
        k: int = 3,
        use_tavily_fallback: bool = True
    ) -> str:
        """
        Retrieve knowledge and format it as context for LLM.
        This is what agents use in their prompts.
        
        Returns:
            Formatted string ready to inject into prompt
        """
        results = await self.retrieve(query, category, k, use_tavily_fallback)
        
        if not results:
            return "No relevant knowledge found."
        
        # Format as context
        context_parts = []
        for i, result in enumerate(results, 1):
            source_type = "Web" if result['metadata'].get('from_tavily') else "Knowledge Base"
            source = result['metadata'].get('source', 'unknown')
            
            context_parts.append(
                f"[Source {i} - {source_type}]\n"
                f"Category: {result['metadata'].get('category', 'unknown')}\n"
                f"{result['document']}\n"
                f"Source: {source}\n"
                f"Relevance: {result['similarity']:.2f}"
            )
        
        return "\n\n---\n\n".join(context_parts)
    
    async def add_knowledge(
        self,
        text: str,
        metadata: Dict[str, Any]
    ):
        """
        Add new knowledge to the RAG system on the fly.
        Used for caching Tavily results or agent learnings.
        
        Args:
            text: Knowledge to add
            metadata: Metadata (category, source, etc.)
        """
        chunks, chunk_metadata = self.document_loader.load_text_directly(
            text, metadata
        )
        
        self.vector_store.add_documents(chunks, chunk_metadata)
        
        # Auto-save after adding (async in background)
        try:
            self.vector_store.save("fitness_knowledge")
        except Exception as e:
            print(f"⚠️  Failed to auto-save RAG: {e}")
    
    # Convenience methods for specific domains
    async def search_fitness_knowledge(
        self, 
        query: str, 
        k: int = 3,
        use_web: bool = True
    ) -> str:
        """Search fitness knowledge (RAG + Tavily fallback)"""
        return await self.retrieve_with_context(
            query, 
            category="fitness", 
            k=k, 
            use_tavily_fallback=use_web
        )
    
    async def search_nutrition_knowledge(
        self, 
        query: str, 
        k: int = 3,
        use_web: bool = True
    ) -> str:
        """Search nutrition knowledge (RAG + Tavily fallback)"""
        return await self.retrieve_with_context(
            query, 
            category="nutrition", 
            k=k, 
            use_tavily_fallback=use_web
        )
    
    async def search_recovery_knowledge(
        self, 
        query: str, 
        k: int = 3,
        use_web: bool = True
    ) -> str:
        """Search recovery knowledge (RAG + Tavily fallback)"""
        return await self.retrieve_with_context(
            query, 
            category="recovery", 
            k=k, 
            use_tavily_fallback=use_web
        )
    
    async def search_psychology_knowledge(
        self, 
        query: str, 
        k: int = 3,
        use_web: bool = True
    ) -> str:
        """Search resolution psychology knowledge (RAG + Tavily fallback)"""
        return await self.retrieve_with_context(
            query, 
            category="resolution_psychology", 
            k=k, 
            use_tavily_fallback=use_web
        )


# Singleton instance
rag_retriever = RAGRetriever()