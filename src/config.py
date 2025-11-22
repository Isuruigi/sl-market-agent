"""Configuration management for SL Market Agent"""
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
    
    # LangSmith Configuration
    LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "true")
    LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "sl-market-agent")
    
    # Model Configuration
    LLM_MODEL = "llama-3.3-70b-versatile"
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    MAX_TOKENS = 2048
    
    # Embedding Configuration
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    EMBEDDING_DIMENSION = 384
    
    # Memory Configuration
    MAX_CONTEXT_LENGTH = int(os.getenv("MAX_CONTEXT_LENGTH", "4000"))
    VECTOR_STORE_PATH = Path("data/vector_store")
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        errors = []
        
        if not cls.GROQ_API_KEY:
            errors.append("❌ GROQ_API_KEY not set in .env file")
        elif not cls.GROQ_API_KEY.startswith("gsk_"):
            errors.append("❌ GROQ_API_KEY appears invalid (should start with 'gsk_')")
            
        if not cls.LANGSMITH_API_KEY:
            errors.append("⚠️  LANGSMITH_API_KEY not set (optional - for monitoring)")
        elif not cls.LANGSMITH_API_KEY.startswith("lsv2_"):
            errors.append("⚠️  LANGSMITH_API_KEY appears invalid (should start with 'lsv2_')")
        
        # Only fail on critical errors (Groq API key)
        critical_errors = [e for e in errors if e.startswith("❌")]
        if critical_errors:
            print("\n" + "="*60)
            print("CONFIGURATION ERRORS:")
            for error in critical_errors:
                print(f"  {error}")
            print("="*60)
            print("\nPlease fix these issues in your .env file")
            raise ValueError("Configuration validation failed")
        
        # Create necessary directories
        cls.VECTOR_STORE_PATH.mkdir(parents=True, exist_ok=True)
        
        print("✅ Configuration validated successfully")
        print(f"   - GROQ API: Connected")
        if cls.LANGSMITH_API_KEY:
            print(f"   - LangSmith: Enabled")
        else:
            print(f"   - LangSmith: Disabled (optional)")
        print(f"   - Model: {cls.LLM_MODEL}")

# Validate on import - REMOVED to allow handling in UI
# Config.validate()
