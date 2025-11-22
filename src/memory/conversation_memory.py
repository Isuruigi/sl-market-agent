"""Conversation memory management"""

from typing import List, Dict
from collections import deque


class ConversationMemory:
    """Manage conversation history with deque for automatic size limiting"""
    
    def __init__(self, max_turns: int = 10):
        """Initialize conversation memory.
        
        Args:
            max_turns: Maximum number of conversation turns to keep.
        """
        self.max_turns = max_turns
        # *2 for user + assistant per turn
        self.messages = deque(maxlen=max_turns * 2)
        
    def add_user_message(self, content: str):
        """Add user message to history.
        
        Args:
            content: User message content.
        """
        self.messages.append({"role": "user", "content": content})
    
    def add_assistant_message(self, content: str):
        """Add assistant message to history.
        
        Args:
            content: Assistant message content.
        """
        self.messages.append({"role": "assistant", "content": content})
    
    def add_system_message(self, content: str):
        """Add system message to history.
        
        Args:
            content: System message content.
        """
        # System messages don't count toward the limit
        # Insert at the beginning
        messages_list = list(self.messages)
        messages_list.insert(0, {"role": "system", "content": content})
        self.messages.clear()
        for msg in messages_list:
            if msg["role"] != "system":
                self.messages.append(msg)
        # Prepend system message (it will stay even when deque is full)
        self._system_message = {"role": "system", "content": content}
    
    def add_message(self, role: str, content: str):
        """Add a message with specified role.
        
        Args:
            role: Message role (user, assistant, or system).
            content: Message content.
        """
        if role == "system":
            self.add_system_message(content)
        elif role == "user":
            self.add_user_message(content)
        elif role == "assistant":
            self.add_assistant_message(content)
    
    def get_messages(self) -> List[Dict]:
        """Get all messages including system message.
        
        Returns:
            List of message dictionaries.
        """
        messages = []
        if hasattr(self, '_system_message'):
            messages.append(self._system_message)
        messages.extend(list(self.messages))
        return messages
    
    def clear(self):
        """Clear all conversation history."""
        self.messages.clear()
        if hasattr(self, '_system_message'):
            delattr(self, '_system_message')
    
    def get_summary(self) -> str:
        """Get conversation summary.
        
        Returns:
            Human-readable summary string.
        """
        if not self.messages and not hasattr(self, '_system_message'):
            return "No conversation history"
        total = len(self.messages)
        return f"{total} messages in history"


def test_memory():
    """Test conversation memory"""
    print("\n" + "="*60)
    print("TESTING CONVERSATION MEMORY")
    print("="*60 + "\n")
    
    memory = ConversationMemory(max_turns=3)
    
    memory.add_system_message("You are a helpful assistant.")
    memory.add_user_message("Hello!")
    memory.add_assistant_message("Hi! How can I help?")
    memory.add_user_message("What's the GDP of Sri Lanka?")
    memory.add_assistant_message("The GDP is approximately $84 billion USD.")
    
    print(f"Summary: {memory.get_summary()}")
    print(f"Total messages: {len(memory.get_messages())}\n")
    
    for msg in memory.get_messages():
        print(f"  {msg['role']:10s}: {msg['content'][:50]}...")
    
    # Test max_turns limit
    print("\n--- Testing turn limit ---")
    for i in range(5):
        memory.add_user_message(f"Question {i+1}")
        memory.add_assistant_message(f"Answer {i+1}")
    
    print(f"After adding 5 more turns: {memory.get_summary()}")
    print(f"Total messages: {len(memory.get_messages())} (should be capped)")
    
    print("\n" + "="*60)
    print("✅ Memory test complete")
    print("="*60)


if __name__ == "__main__":
    test_memory()
