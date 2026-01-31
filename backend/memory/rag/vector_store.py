# memory/rag/vector_store.py

"""
Vector Store using FAISS - optimized for CPU
"""
import time
import faiss
import numpy as np
import pickle
from typing import List, Dict, Any, Optional
from pathlib import Path
import cohere
from core.config import settings


class VectorStore:
    """FAISS-based vector store for RAG"""
    
    def __init__(self, dimension: int = 1024):  # Cohere embed-english-v3.0 = 1024 dims
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)  # L2 distance, works great on CPU
        self.documents = []  # Store actual documents
        self.metadata = []   # Store metadata (source, category, etc.)
        self.cohere_client = cohere.Client(api_key=settings.COHERE_API_KEY)
        self.store_path = Path("memory/rag/data")
        self.store_path.mkdir(parents=True, exist_ok=True)



    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """Embed texts using Cohere API with retry logic"""
        max_retries = 3
        retry_delay = 60  # seconds
    
        for attempt in range(max_retries):
            try:
                response = self.cohere_client.embed(
                    texts=texts,
                    model="embed-english-v3.0",
                    input_type="search_document"
                )
                return np.array(response.embeddings, dtype=np.float32)
            
            except Exception as e:
                if "429" in str(e) and attempt < max_retries - 1:
                    print(f"⏳ Rate limited. Waiting {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(retry_delay)
                else:
                    print(f"Embedding error: {e}")
                    raise


    def embed_query(self, query: str) -> np.ndarray:
        """Embed a search query"""
        try:
            response = self.cohere_client.embed(
                texts=[query],
                model="embed-english-v3.0",
                input_type="search_query"  # For search queries
            )
            return np.array(response.embeddings[0], dtype=np.float32)
        except Exception as e:
            print(f"Query embedding error: {e}")
            raise
    
    def add_documents(self, documents: List[str], metadata: Optional[List[Dict[str, Any]]] = None):
        """Add documents to the vector store with batching"""
        if not documents:
            return
    
        batch_size = 5  # Process 5 at a time to avoid rate limits
    
        for i in range(0, len(documents), batch_size):
            batch_docs = documents[i:i + batch_size]
            batch_meta = metadata[i:i + batch_size] if metadata else None
        
        # Embed batch
        embeddings = self.embed_texts(batch_docs)
        
        # Add to FAISS index
        self.index.add(embeddings)
        
        # Store documents and metadata
        self.documents.extend(batch_docs)
        if batch_meta:
            self.metadata.extend(batch_meta)
        else:
            self.metadata.extend([{}] * len(batch_docs))
        
        print(f"✅ Processed batch {i//batch_size + 1}: {len(batch_docs)} docs")
        
        # Small delay between batches
        if i + batch_size < len(documents):
            time.sleep(2)  # 2 second pause between batches
    
        print(f"✅ Total documents added: {len(documents)}")

    def search(
        self, 
        query: str, 
        k: int = 5,
        filter_category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        if len(self.documents) == 0:
            return []
        
        # Embed query
        query_vector = self.embed_query(query)
        
        # Search FAISS
        distances, indices = self.index.search(
            query_vector.reshape(1, -1), 
            k * 2  # Get more results for filtering
        )
        
        # Format results
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx >= len(self.documents):  # Safety check
                continue
            
            meta = self.metadata[idx]
            
            # Apply category filter if specified
            if filter_category and meta.get("category") != filter_category:
                continue
            
            results.append({
                "document": self.documents[idx],
                "metadata": meta,
                "distance": float(dist),
                "similarity": 1 / (1 + float(dist))  # Convert distance to similarity
            })
            
            if len(results) >= k:
                break
        
        return results
    
    def save(self, name: str = "fitness_knowledge"):
        """Save index and documents to disk"""
        # Save FAISS index
        faiss.write_index(self.index, str(self.store_path / f"{name}.index"))
        
        # Save documents and metadata
        with open(self.store_path / f"{name}.pkl", "wb") as f:
            pickle.dump({
                "documents": self.documents,
                "metadata": self.metadata
            }, f)
        
        print(f"✅ Saved vector store: {name}")
    
    def load(self, name: str = "fitness_knowledge"):
        """Load index and documents from disk"""
        index_path = self.store_path / f"{name}.index"
        data_path = self.store_path / f"{name}.pkl"
        
        if not index_path.exists() or not data_path.exists():
            print(f"⚠️  Vector store '{name}' not found")
            return False
        
        # Load FAISS index
        self.index = faiss.read_index(str(index_path))
        
        # Load documents and metadata
        with open(data_path, "rb") as f:
            data = pickle.load(f)
            self.documents = data["documents"]
            self.metadata = data["metadata"]
        
        print(f"✅ Loaded {len(self.documents)} documents from '{name}'")
        return True


# Singleton instance
vector_store = VectorStore()