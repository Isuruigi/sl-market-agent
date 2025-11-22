"""GROQ LLM Wrapper using LangChain"""

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from typing import List, Dict, Optional
import time
from ..config import Config


class GroqLLM:
    """Production-ready GROQ LLM wrapper with retry logic and monitoring"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Groq LLM with LangChain.
        
        Args:
            api_key: Groq API key. If None, uses the key from Config.
        """
        self.api_key = api_key or Config.GROQ_API_KEY
        self.llm = ChatGroq(
            groq_api_key=self.api_key,
            model_name=Config.LLM_MODEL,
            temperature=Config.TEMPERATURE,
            max_tokens=Config.MAX_TOKENS
        )
        self.call_count = 0
    
    def _format_messages(self, messages: List[Dict[str, str]]) -> List:
        """Convert dict messages to LangChain message objects.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'.
            
        Returns:
            List of LangChain message objects.
        """
        formatted = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            
            if role == "system":
                formatted.append(SystemMessage(content=content))
            elif role == "user":
                formatted.append(HumanMessage(content=content))
            elif role == "assistant":
                formatted.append(AIMessage(content=content))
        
        return formatted
    
    def generate(
        self, 
        messages: List[Dict[str, str]], 
        max_retries: int = 3
    ) -> str:
        """Generate response with retry logic.
        
        Args:
            messages: List of message dictionaries.
            max_retries: Maximum number of retry attempts.
            
        Returns:
            Generated response string.
            
        Raises:
            Exception: If all retry attempts fail.
        """
        for attempt in range(max_retries):
            try:
                start = time.time()
                formatted = self._format_messages(messages)
                response = self.llm.invoke(formatted)
                elapsed = time.time() - start
                
                self.call_count += 1
                print(f"✅ LLM call #{self.call_count} ({elapsed:.1f}s)")
                
                return response.content
                
            except Exception as e:
                if attempt < max_retries - 1:
                    wait = 2 ** attempt
                    print(f"⚠️  Retry {attempt + 1}/{max_retries} in {wait}s...")
                    time.sleep(wait)
                else:
                    raise Exception(f"LLM failed after {max_retries} attempts: {e}")
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Send a chat completion request (for compatibility).
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'.
            temperature: Sampling temperature (not used in this version).
            max_tokens: Maximum tokens to generate (not used in this version).
            
        Returns:
            The assistant's response as a string.
        """
        return self.generate(messages)
    
    def simple_chat(self, prompt: str) -> str:
        """Simple single-turn chat.
        
        Args:
            prompt: User prompt.
            
        Returns:
            Generated response.
        """
        return self.generate([{"role": "user", "content": prompt}])
    
    def stream(self, messages: List[Dict[str, str]]):
        """Stream responses from the LLM.
        
        Args:
            messages: List of message dictionaries.
            
        Yields:
            Chunks of the response as they arrive.
        """
        formatted = self._format_messages(messages)
        for chunk in self.llm.stream(formatted):
            yield chunk.content


def test_llm():
    """Test LLM functionality"""
    print("\n" + "="*60)
    print("TESTING GROQ LLM")
    print("="*60 + "\n")
    
    llm = GroqLLM()
    
    print("Test 1: Simple question")
    response = llm.simple_chat("What is the capital of Sri Lanka? Answer in one sentence.")
    print(f"Response: {response}\n")
    
    print("Test 2: Conversation")
    messages = [
        {"role": "system", "content": "You are an expert on Sri Lankan economics."},
        {"role": "user", "content": "What are Sri Lanka's main exports?"}
    ]
    response = llm.generate(messages)
    print(f"Response: {response}\n")
    
    print("="*60)
    print(f"✅ All tests passed! Total calls: {llm.call_count}")
    print("="*60)


if __name__ == "__main__":
    test_llm()
