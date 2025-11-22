"""Simple RAG system with vector storage using sentence transformers"""

from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict, Optional
import pickle
from pathlib import Path
from ..config import Config


class VectorStore:
    """Simple RAG with sentence transformers and numpy similarity search"""
    
    def __init__(self, collection_name: str = "market_data"):
        """Initialize the vector store.
        
        Args:
            collection_name: Name of the collection (used for file naming).
        """
        self.collection_name = collection_name
        print("📦 Loading embedding model...")
        self.encoder = SentenceTransformer(Config.EMBEDDING_MODEL)
        self.documents = []
        self.embeddings = None
        self.store_path = Config.VECTOR_STORE_PATH / f"{collection_name}.pkl"
        
        # Try to load existing store
        self._load()
    
    def add_documents(
        self,
        documents: List[str],
        metadatas: Optional[List[Dict]] = None,
        ids: Optional[List[str]] = None,
        chunk: bool = False
    ):
        """Add documents to the knowledge base.
        
        Args:
            documents: List of document texts.
            metadatas: Optional list of metadata dictionaries (not used in simple version).
            ids: Optional list of document IDs (not used in simple version).
            chunk: Whether to chunk documents (not implemented in simple version).
        """
        if not documents:
            return
        
        print(f"📝 Adding {len(documents)} documents...")
        new_embeddings = self.encoder.encode(documents, show_progress_bar=False)
        
        self.documents.extend(documents)
        
        if self.embeddings is None:
            self.embeddings = new_embeddings
        else:
            self.embeddings = np.vstack([self.embeddings, new_embeddings])
        
        print(f"✅ Total documents: {len(self.documents)}")
        self._save()
    
    def query(
        self,
        query_text: str,
        n_results: int = 5,
        filter_dict: Optional[Dict] = None
    ) -> List[Dict]:
        """Search for relevant documents.
        
        Args:
            query_text: Query text.
            n_results: Number of results to return.
            filter_dict: Optional metadata filter (not used in simple version).
            
        Returns:
            List of result dictionaries with text and score.
        """
        if not self.documents:
            return []
        
        query_embedding = self.encoder.encode([query_text])[0]
        
        # Compute cosine similarity
        similarities = np.dot(self.embeddings, query_embedding)
        
        # Get top k indices
        top_k = min(n_results, len(self.documents))
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            results.append({
                "text": self.documents[idx],
                "score": float(similarities[idx])
            })
        
        return results
    
    def get_relevant_context(
        self,
        query: str,
        n_results: int = 3
    ) -> List[str]:
        """Get relevant context documents for a query.
        
        Args:
            query: Query text.
            n_results: Number of results to return.
            
        Returns:
            List of relevant document texts.
        """
        results = self.query(query, n_results)
        return [result["text"] for result in results]
    
    def similarity_search_with_score(
        self,
        query: str,
        k: int = 3
    ) -> List[tuple]:
        """Search with similarity scores.
        
        Args:
            query: Query text.
            k: Number of results.
            
        Returns:
            List of (text, score) tuples.
        """
        results = self.query(query, k)
        return [(result["text"], result["score"]) for result in results]
    
    def format_context(self, results: List[Dict]) -> str:
        """Format search results for LLM context.
        
        Args:
            results: List of search results.
            
        Returns:
            Formatted context string.
        """
        if not results:
            return ""
        
        context = "Relevant information from knowledge base:\n\n"
        for i, result in enumerate(results, 1):
            context += f"[{i}] {result['text']}\n\n"
        
        return context
    
    def _save(self):
        """Save store to disk."""
        Config.VECTOR_STORE_PATH.mkdir(parents=True, exist_ok=True)
        data = {
            "documents": self.documents,
            "embeddings": self.embeddings
        }
        with open(self.store_path, 'wb') as f:
            pickle.dump(data, f)
    
    def _load(self):
        """Load store from disk."""
        if self.store_path.exists():
            try:
                with open(self.store_path, 'rb') as f:
                    data = pickle.load(f)
                    self.documents = data["documents"]
                    self.embeddings = data["embeddings"]
                print(f"✅ Loaded {len(self.documents)} documents from storage")
            except Exception as e:
                print(f"⚠️  Could not load vector store: {e}")
    
    def clear(self):
        """Clear all documents from the collection."""
        self.documents = []
        self.embeddings = None
        if self.store_path.exists():
            self.store_path.unlink()
        print("🗑️  Vector store cleared")
    
    def count(self) -> int:
        """Get the number of documents in the collection.
        
        Returns:
            Number of documents.
        """
        return len(self.documents)
    
    def as_retriever(self, **kwargs):
        """Get a retriever interface (placeholder for LangChain compatibility).
        
        Returns:
            Self as a simple retriever.
        """
        return self


def test_rag():
    """Test RAG system"""
    print("\n" + "="*60)
    print("TESTING RAG SYSTEM")
    print("="*60 + "\n")
    
    rag = VectorStore("test_collection")
    
    # Clear any existing data
    rag.clear()
    
    # Add sample documents
    docs = [
        "Sri Lanka's GDP growth was 5.3% in 2023.",
        "The Central Bank of Sri Lanka manages monetary policy.",
        "Tea is Sri Lanka's largest export commodity.",
        "Colombo is the commercial capital of Sri Lanka.",
        "The main industries include tourism, textiles, and agriculture.",
    ]
    
    rag.add_documents(docs)
    
    # Test search
    query = "What is Sri Lanka's economic growth?"
    print(f"Query: {query}")
    results = rag.query(query, n_results=2)
    
    print(f"\nTop {len(results)} results:")
    for result in results:
        print(f"  Score: {result['score']:.3f}")
        print(f"  Text: {result['text']}\n")
    
    # Test context retrieval
    context = rag.get_relevant_context("exports", n_results=2)
    print(f"Context for 'exports': {len(context)} documents")
    for doc in context:
        print(f"  - {doc}")
    
    print("\n" + "="*60)
    print(f"✅ RAG test complete - {rag.count()} documents stored")
    print("="*60)
    
    # Cleanup
    rag.clear()


if __name__ == "__main__":
    test_rag()
