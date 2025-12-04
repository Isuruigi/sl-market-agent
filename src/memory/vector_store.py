"""Simple RAG system with TF-IDF vectorization (lightweight, no PyTorch needed)"""

import numpy as np
from typing import List, Dict, Optional
import pickle
from pathlib import Path
import os

# Try to import sklearn, fallback to simple keyword matching if not available
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False


class VectorStore:
    """Lightweight RAG with TF-IDF vectorization (works on Streamlit Cloud)"""
    
    def __init__(self, collection_name: str = "market_data"):
        """Initialize the vector store.
        
        Args:
            collection_name: Name of the collection (used for file naming).
        """
        self.collection_name = collection_name
        self.documents = []
        self.vectorizer = None
        self.tfidf_matrix = None
        
        # Use a simple path that works on Streamlit Cloud
        self.store_path = Path("data") / "vector_store" / f"{collection_name}.pkl"
        
        print("📦 Initializing lightweight vector store (TF-IDF)...")
        
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
            metadatas: Optional list of metadata dictionaries (not used).
            ids: Optional list of document IDs (not used).
            chunk: Whether to chunk documents (not used).
        """
        if not documents:
            return
        
        print(f"📝 Adding {len(documents)} documents...")
        self.documents.extend(documents)
        
        # Rebuild TF-IDF matrix with all documents
        self._rebuild_index()
        
        print(f"✅ Total documents: {len(self.documents)}")
        self._save()
    
    def _rebuild_index(self):
        """Rebuild the TF-IDF index."""
        if not self.documents:
            self.vectorizer = None
            self.tfidf_matrix = None
            return
        
        if HAS_SKLEARN:
            self.vectorizer = TfidfVectorizer(
                stop_words='english',
                max_features=5000,
                ngram_range=(1, 2)
            )
            self.tfidf_matrix = self.vectorizer.fit_transform(self.documents)
        else:
            # Fallback: simple word frequency
            self.vectorizer = None
            self.tfidf_matrix = None
    
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
            filter_dict: Optional metadata filter (not used).
            
        Returns:
            List of result dictionaries with text and score.
        """
        if not self.documents:
            return []
        
        if HAS_SKLEARN and self.vectorizer is not None:
            # TF-IDF based search
            query_vec = self.vectorizer.transform([query_text])
            similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        else:
            # Fallback: simple keyword matching
            query_words = set(query_text.lower().split())
            similarities = []
            for doc in self.documents:
                doc_words = set(doc.lower().split())
                overlap = len(query_words & doc_words)
                score = overlap / max(len(query_words), 1)
                similarities.append(score)
            similarities = np.array(similarities)
        
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
        try:
            self.store_path.parent.mkdir(parents=True, exist_ok=True)
            data = {
                "documents": self.documents,
            }
            with open(self.store_path, 'wb') as f:
                pickle.dump(data, f)
        except Exception as e:
            print(f"⚠️  Could not save vector store: {e}")
    
    def _load(self):
        """Load store from disk."""
        if self.store_path.exists():
            try:
                with open(self.store_path, 'rb') as f:
                    data = pickle.load(f)
                    self.documents = data.get("documents", [])
                    self._rebuild_index()
                print(f"✅ Loaded {len(self.documents)} documents from storage")
            except Exception as e:
                print(f"⚠️  Could not load vector store: {e}")
    
    def clear(self):
        """Clear all documents from the collection."""
        self.documents = []
        self.vectorizer = None
        self.tfidf_matrix = None
        if self.store_path.exists():
            try:
                self.store_path.unlink()
            except:
                pass
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
    print("TESTING RAG SYSTEM (TF-IDF)")
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
