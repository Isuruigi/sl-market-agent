"""GROQ LLM Wrapper using direct Groq SDK (lightweight, no LangChain)"""

import os
import time
from typing import List, Dict, Optional

# Import Groq SDK
try:
    from groq import Groq
    HAS_GROQ = True
except ImportError:
    HAS_GROQ = False
    Groq = None


class GroqLLM:
    """Production-ready GROQ LLM wrapper with retry logic"""
    
    # Default configuration
    DEFAULT_MODEL = "llama-3.3-70b-versatile"
    DEFAULT_TEMPERATURE = 0.7
    DEFAULT_MAX_TOKENS = 2048
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Groq LLM.
        
        Args:
            api_key: Groq API key. If None, uses GROQ_API_KEY env var.
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        if not HAS_GROQ:
            raise ImportError("groq package not installed. Run: pip install groq")
        
        self.client = Groq(api_key=self.api_key)
        self.model = os.getenv("LLM_MODEL", self.DEFAULT_MODEL)
        self.temperature = float(os.getenv("TEMPERATURE", str(self.DEFAULT_TEMPERATURE)))
        self.max_tokens = int(os.getenv("MAX_TOKENS", str(self.DEFAULT_MAX_TOKENS)))
        self.call_count = 0
    
    def generate(
        self, 
        messages: List[Dict[str, str]], 
        max_retries: int = 3
    ) -> str:
        """Generate response with retry logic.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'.
            max_retries: Maximum number of retry attempts.
            
        Returns:
            Generated response string.
            
        Raises:
            Exception: If all retry attempts fail.
        """
        for attempt in range(max_retries):
            try:
                start = time.time()
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens
                )
                
                elapsed = time.time() - start
                self.call_count += 1
                print(f"✅ LLM call #{self.call_count} ({elapsed:.1f}s)")
                
                return response.choices[0].message.content
                
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
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            stream=True
        )
        
        for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


def test_llm():
    """Test LLM functionality"""
    print("\n" + "="*60)
    print("TESTING GROQ LLM (Direct SDK)")
    print("="*60 + "\n")
    
    llm = GroqLLM()
    
    print("Test 1: Simple question")
    response = llm.simple_chat("What is the capital of Sri Lanka? Answer in one sentence.")
    print(f"Response: {response}\n")
    
    print("Test 2: Conversation")
    messages = [
        {"role": "system", "content": "You are an expert on Sri Lankan economics."},
        {"role": "user", "content": "What are Sri Lanka's main exports? Answer briefly."}
    ]
    response = llm.generate(messages)
    print(f"Response: {response}\n")
    
    print("="*60)
    print(f"✅ All tests passed! Total calls: {llm.call_count}")
    print("="*60)


if __name__ == "__main__":
    test_llm()
