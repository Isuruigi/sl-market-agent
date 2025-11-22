"""Main application entry point for the Market Agent."""

import sys
from src.agent import MarketAgent
from src.config import Config


def print_banner():
    """Print application banner."""
    print("=" * 60)
    print("🤖 SL Market Agent - Intelligent Market Analysis Assistant")
    print("=" * 60)
    print("Powered by Groq + Sentence-Transformers + Production-Ready Tools")
    print()


def print_help():
    """Print help information."""
    print("\n📋 Commands:")
    print("  /help      - Show this help message")
    print("  /reset     - Reset conversation history")
    print("  /tools     - List available tools")
    print("  /verbose   - Toggle verbose mode (see agent reasoning)")
    print("  /clear     - Clear knowledge base")
    print("  /add       - Add text to knowledge base")
    print("  /quit      - Exit the application")
    print()


def main():
    """Run the main application."""
    print_banner()
    
    # Validate configuration
    try:
        Config.validate()
    except ValueError:
        return
    try:
        agent = MarketAgent(verbose=False)
        verbose_mode = False
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        print("\nPlease check your configuration and try again.")
        return
    
    print("Welcome! I'm your market analysis assistant.")
    print("I can help with calculations, web scraping, and knowledge search.")
    print("Type /help for available commands.\n")
    
    # Main interaction loop
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.startswith("/"):
                command = user_input.lower()
                
                if command == "/quit" or command == "/exit":
                    print("\n👋 Goodbye! Thanks for using Market Agent.")
                    break
                
                elif command == "/help":
                    print_help()
                    continue
                
                elif command == "/reset":
                    agent.reset()
                    continue
                
                elif command == "/tools":
                    print("\n🛠️  Available Tools:")
                    tools = agent.get_tools_info()
                    for tool in tools:
                        print(f"  • {tool['name']}: {tool['description'][:80]}...")
                    print()
                    continue
                
                elif command == "/verbose":
                    verbose_mode = not verbose_mode
                    agent.verbose = verbose_mode
                    status = "enabled" if verbose_mode else "disabled"
                    print(f"🔧 Verbose mode {status}\n")
                    continue
                
                elif command == "/clear":
                    agent.clear_knowledge()
                    continue
                
                elif command == "/add":
                    print("Enter text to add to knowledge base (press Enter twice when done):")
                    lines = []
                    while True:
                        line = input()
                        if line == "":
                            break
                        lines.append(line)
                    if lines:
                        text = "\n".join(lines)
                        agent.add_knowledge([text])
                    continue
                
                else:
                    print(f"❌ Unknown command: {user_input}")
                    print("Type /help for available commands.\n")
                    continue
            
            # Get agent response
            print("\n🤖 Agent: ", end="", flush=True)
            response = agent.chat(user_input)
            print(response)
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thanks for using Market Agent.")
            break
        
        except Exception as e:
            print(f"\n❌ Error: {e}")
            if verbose_mode:
                import traceback
                traceback.print_exc()
            print("Please try again.\n")


if __name__ == "__main__":
    main()
