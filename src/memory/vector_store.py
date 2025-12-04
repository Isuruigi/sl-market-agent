"""Simple keyword-based search (no external ML dependencies)"""

from typing import List, Dict, Optional
import pickle
from pathlib import Path
import re


class VectorStore:
    """Simple keyword-based search (works anywhere, no dependencies)"""
    
    def __init__(self, collection_name: str = "market_data"):
        """Initialize the vector store.
        
        Args:
            collection_name: Name of the collection.
        """
        self.collection_name = collection_name
        self.documents = []
        
        # Simple path that works on Streamlit Cloud
        self.store_path = Path("data") / "vector_store" / f"{collection_name}.pkl"
        
        print("📦 Initializing keyword-based search...")
        self._load()
    
    def _tokenize(self, text: str) -> set:
        """Simple tokenization."""
        # Lowercase, remove punctuation, split on whitespace
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        words = set(text.split())
        # Remove very short words
        return {w for w in words if len(w) > 2}
    
    def add_documents(
        self,
        documents: List[str],
        metadatas: Optional[List[Dict]] = None,
        ids: Optional[List[str]] = None,
        chunk: bool = False
    ):
        """Add documents to the knowledge base."""
        if not documents:
            return
        
        print(f"📝 Adding {len(documents)} documents...")
        self.documents.extend(documents)
        print(f"✅ Total documents: {len(self.documents)}")
        self._save()
    
    def query(
        self,
        query_text: str,
        n_results: int = 5,
        filter_dict: Optional[Dict] = None
    ) -> List[Dict]:
        """Search for relevant documents using keyword matching."""
        if not self.documents:
            return []
        
        query_tokens = self._tokenize(query_text)
        
        # Score each document by keyword overlap
        scores = []
        for doc in self.documents:
            doc_tokens = self._tokenize(doc)
            # Jaccard-like overlap score
            overlap = len(query_tokens & doc_tokens)
            score = overlap / max(len(query_tokens), 1)
            scores.append(score)
        
        # Get top k
        top_k = min(n_results, len(self.documents))
        indexed_scores = [(i, s) for i, s in enumerate(scores)]
        indexed_scores.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for idx, score in indexed_scores[:top_k]:
            results.append({
                "text": self.documents[idx],
                "score": score
            })
        
        return results
    
    def get_relevant_context(
        self,
        query: str,
        n_results: int = 3
    ) -> List[str]:
        """Get relevant context documents."""
        results = self.query(query, n_results)
        return [result["text"] for result in results]
    
    def similarity_search_with_score(
        self,
        query: str,
        k: int = 3
    ) -> List[tuple]:
        """Search with similarity scores."""
        results = self.query(query, k)
        return [(result["text"], result["score"]) for result in results]
    
    def format_context(self, results: List[Dict]) -> str:
        """Format search results for LLM context."""
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
            with open(self.store_path, 'wb') as f:
                pickle.dump({"documents": self.documents}, f)
        except Exception as e:
            print(f"⚠️  Could not save: {e}")
    
    def _load(self):
        """Load store from disk."""
        if self.store_path.exists():
            try:
                with open(self.store_path, 'rb') as f:
                    data = pickle.load(f)
                    self.documents = data.get("documents", [])
                print(f"✅ Loaded {len(self.documents)} documents")
            except Exception as e:
                print(f"⚠️  Could not load: {e}")
    
    def clear(self):
        """Clear all documents."""
        self.documents = []
        if self.store_path.exists():
            try:
                self.store_path.unlink()
            except:
                pass
        print("🗑️  Cleared")
    
    def count(self) -> int:
        """Get document count."""
        return len(self.documents)
    
    def as_retriever(self, **kwargs):
        """LangChain compatibility placeholder."""
        return self


def test_rag():
    """Test the search system"""
    print("\n" + "="*60)
    print("TESTING KEYWORD SEARCH")
    print("="*60 + "\n")
    
    rag = VectorStore("test")
    rag.clear()
    
    docs = [
        "Sri Lanka's GDP growth was 5.3% in 2023.",
        "Tea is Sri Lanka's largest export commodity.",
        "Colombo is the commercial capital.",
    ]
    
    rag.add_documents(docs)
    
    results = rag.query("GDP economic growth", n_results=2)
    print(f"Query: GDP economic growth")
    print(f"Results: {len(results)}")
    for r in results:
        print(f"  - Score {r['score']:.2f}: {r['text'][:50]}...")
    
    print("\n✅ Test complete")
    rag.clear()


if __name__ == "__main__":
    test_rag()
