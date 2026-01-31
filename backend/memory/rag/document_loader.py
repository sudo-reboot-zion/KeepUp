"""
Document Loader - Load and chunk documents for RAG
"""
from typing import List, Dict, Any
from pathlib import Path
import re


class DocumentLoader:
    """
    Loads documents from files and chunks them for embedding.
    Supports: .txt, .md
    """
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        """
        Args:
            chunk_size: Target size of each chunk (in characters)
            chunk_overlap: Overlap between chunks (helps with context)
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def load_file(self, file_path: Path) -> str:
        """Load a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return ""
    
    def load_directory(
        self, 
        directory: Path, 
        file_extensions: List[str] = [".txt", ".md"]
    ) -> List[Dict[str, Any]]:
        """
        Load all documents from a directory.
        
        Returns:
            List of dicts with 'content', 'source', 'category'
        """
        documents = []
        
        if not directory.exists():
            print(f"⚠️  Directory not found: {directory}")
            return documents
        
        for file_path in directory.rglob("*"):
            if file_path.suffix in file_extensions:
                content = self.load_file(file_path)
                if content:
                    # Extract category from parent folder
                    category = file_path.parent.name
                    
                    documents.append({
                        "content": content,
                        "source": str(file_path),
                        "category": category,
                        "filename": file_path.name
                    })
        
        print(f"✅ Loaded {len(documents)} documents from {directory}")
        return documents
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into chunks with overlap.
        Tries to split on sentence boundaries.
        """
        if len(text) <= self.chunk_size:
            return [text]
        
        # Split on sentence endings
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            # If adding this sentence exceeds chunk_size, save current chunk
            if len(current_chunk) + len(sentence) > self.chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                # Start new chunk with overlap from previous
                overlap_text = current_chunk[-self.chunk_overlap:] if len(current_chunk) > self.chunk_overlap else current_chunk
                current_chunk = overlap_text + " " + sentence
            else:
                current_chunk += " " + sentence
        
        # Add final chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def load_and_chunk(
        self, 
        directory: Path,
        file_extensions: List[str] = [".txt", ".md"]
    ) -> tuple[List[str], List[Dict[str, Any]]]:
        """
        Load documents and chunk them.
        
        Returns:
            (chunks, metadata) - Ready for vector_store.add_documents()
        """
        documents = self.load_directory(directory, file_extensions)
        
        all_chunks = []
        all_metadata = []
        
        for doc in documents:
            chunks = self.chunk_text(doc["content"])
            
            for i, chunk in enumerate(chunks):
                all_chunks.append(chunk)
                all_metadata.append({
                    "source": doc["source"],
                    "category": doc["category"],
                    "filename": doc["filename"],
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                })
        
        print(f"✅ Created {len(all_chunks)} chunks from {len(documents)} documents")
        return all_chunks, all_metadata
    
    def load_text_directly(self, text: str, metadata: Dict[str, Any]) -> tuple[List[str], List[Dict[str, Any]]]:
        """
        Load text directly (not from file) and chunk it.
        Useful for adding custom knowledge.
        """
        chunks = self.chunk_text(text)
        metadata_list = [metadata.copy() for _ in chunks]
        
        return chunks, metadata_list


# Singleton instance
document_loader = DocumentLoader(chunk_size=500, chunk_overlap=50)