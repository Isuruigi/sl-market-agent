"""Sri Lankan Market Intelligence Agent - Simple Implementation"""

from typing import List, Dict
import re

from ..llm.groq_llm import GroqLLM
from ..tools.calculator import SafeCalculator
from ..tools.web_scraper import scrape_webpage
from ..memory.conversation_memory import ConversationMemory
from ..memory.vector_store import VectorStore


class MarketAgent:
    """Simple Market Intelligence Agent for Sri Lankan markets"""
    
    def __init__(self, verbose: bool = True):
        """Initialize the market agent.
        
        Args:
            verbose: Whether to print agent reasoning steps.
        """
        print("\n🤖 Initializing Sri Lankan Market Agent...")
        print("="*60)
        
        # Initialize components
        self.llm = GroqLLM()
        self.calculator = SafeCalculator()
        self.memory = ConversationMemory(max_turns=10)
        self.rag = VectorStore("market_knowledge")
        self.verbose = verbose
        
        # System prompt
        self.system_prompt = """You are an expert assistant for Sri Lankan market intelligence and economics.

You have access to these tools:
1. Calculator - For mathematical calculations 
2. WebScraper - To scrape content from URLs
3. SearchKnowledge - To search the knowledge base

When you need to use a tool, respond in this format:
USE_TOOL: tool_name
INPUT: input_value

Available tools:
- Calculator: Use for math like "100 * 1.05" or "(250-50)/4"
- WebScraper: Use with a URL to fetch web content  
- SearchKnowledge: Use with a query to search knowledge base

Think step by step and provide clear, actionable insights."""
        
        print("✅ Agent initialized successfully")
        print("="*60 + "\n")
    
    def _check_tool_use(self, response: str) -> tuple:
        """Check if the LLM wants to use a tool.
        
        Args:
            response: LLM response.
            
        Returns:
            Tuple of (tool_name, input_value) or (None, None).
        """
        if "USE_TOOL:" in response:
            lines = response.split("\n")
            tool_name = None
            input_value = None
            
            for i, line in enumerate(lines):
                if line.startswith("USE_TOOL:"):
                   tool_name = line.replace("USE_TOOL:", "").strip()
                elif line.startswith("INPUT:"):
                    input_value = line.replace("INPUT:", "").strip()
            
            return (tool_name, input_value)
        
        return (None, None)
    
    def _execute_tool(self, tool_name: str, tool_input: str) -> str:
        """Execute a tool.
        
        Args:
            tool_name: Name of tool to execute.
            tool_input: Input for the tool.
            
        Returns:
            Tool result.
        """
        if self.verbose:
            print(f"\n🔧 Using {tool_name} with input: {tool_input}")
        
        try:
            if tool_name.lower() == "calculator":
                result = self.calculator.calculate(tool_input)
                return result
            
            elif tool_name.lower() == "webscraper":
                result = scrape_webpage(tool_input)
                return result
            
            elif tool_name.lower() == "searchknowledge":
                results = self.rag.query(tool_input, n_results=2)
                if not results:
                    return "No relevant information found in knowledge base."
                return self.rag.format_context(results)
            
            else:
                return f"Unknown tool: {tool_name}"
        
        except Exception as e:
            return f"Tool error: {str(e)}"
    
    def chat(self, user_input: str) -> str:
        """Chat with the agent.
        
        Args:
            user_input: User's question or message.
            
        Returns:
            Agent's response.
        """
        try:
            # Add to memory
            self.memory.add_user_message(user_input)
            
            # Get conversation history
            messages = self.memory.get_messages()
            
            # Initial response
            response = self.llm.generate(messages)
            
            if self.verbose:
                print(f"\n💭 Initial thought: {response[:100]}...")
            
            # Check if tool use is needed (max 3 iterations)
            for iteration in range(3):
                tool_name, tool_input = self._check_tool_use(response)
                
                if tool_name and tool_input:
                    # Execute tool
                    tool_result = self._execute_tool(tool_name, tool_input)
                    
                    # Add tool result to context
                    messages.append({
                        "role": "assistant",
                        "content": f"I used {tool_name} and got: {tool_result}"
                    })
                    messages.append({
                        "role": "user",
                        "content": "Now provide the final answer based on the tool result."
                    })
                    
                    # Get final response
                    response = self.llm.generate(messages)
                    
                    if self.verbose:
                        print(f"\n✅ Tool result: {tool_result[:100]}...")
                else:
                    # No tool use needed, this is the final answer
                    break
            
            # Clean up response
            final_answer = response.replace("USE_TOOL:", "").replace("INPUT:", "").strip()
            
            # Add to memory
            self.memory.add_assistant_message(final_answer)
            
            # Store in RAG
            conversation_text = f"User asked: {user_input}\nAgent answered: {final_answer}"
            self.rag.add_documents([conversation_text], chunk=False)
            
            return final_answer
            
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            if self.verbose:
                import traceback
                traceback.print_exc()
            self.memory.add_assistant_message(error_msg)
            return error_msg
    
    def add_knowledge(self, documents: List[str]):
        """Add documents to knowledge base.
        
        Args:
            documents: List of document texts to add.
        """
        self.rag.add_documents(documents, chunk=False)
        print(f"✅ Added {len(documents)} documents to knowledge base")
    
    def reset(self):
        """Reset conversation memory."""
        self.memory.clear()
        print("🔄 Conversation memory reset")
    
    def clear_knowledge(self):
        """Clear knowledge base."""
        self.rag.clear()
        print("🗑️  Knowledge base cleared")
    
    def get_tools_info(self) -> List[Dict]:
        """Get information about available tools.
        
        Returns:
            List of tool information dictionaries.
        """
        return [
            {"name": "Calculator", "description": "Perform mathematical calculations"},
            {"name": "WebScraper", "description": "Scrape content from web pages"},
            {"name": "SearchKnowledge", "description": "Search the knowledge base"}
        ]


def test_agent():
    """Test the agent"""
    print("\n" + "="*60)
    print("TESTING MARKET AGENT")
    print("="*60 + "\n")
    
    agent = MarketAgent(verbose=True)
    
    # Add some knowledge
    print("\n📚 Adding knowledge to the system...")
    knowledge = [
        "Sri Lanka's main exports include tea, textiles, and rubber products.",
        "The Central Bank of Sri Lanka is the monetary authority responsible for monetary policy.",
        "Tourism is a major contributor to Sri Lanka's economy, generating significant foreign exchange.",
        "The Colombo Stock Exchange (CSE) is the main stock exchange in Sri Lanka.",
    ]
    agent.add_knowledge(knowledge)
    
    # Test questions
    questions = [
        "What are Sri Lanka's main exports?",
        "What is 25% of 10000?",
    ]
    
    for question in questions:
        print(f"\n{'='*60}")
        print(f"❓ Question: {question}")
        print("="*60)
        answer = agent.chat(question)
        print(f"\n💬 Final Answer: {answer}")
        print("="*60)
    
    print("\n" + "="*60)
    print("✅ Agent test complete")
    print("="*60)


if __name__ == "__main__":
    test_agent()
