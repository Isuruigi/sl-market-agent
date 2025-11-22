"""Tests for agent module."""

import pytest
from src.agent import MarketAgent


def test_agent_initialization():
    """Test agent initialization."""
    agent = MarketAgent()
    assert agent is not None
    assert agent.llm is not None
    assert agent.tools is not None
    assert agent.memory is not None
    assert agent.vector_store is not None


def test_agent_tools_info():
    """Test getting tools information."""
    agent = MarketAgent()
    tools = agent.get_tools_info()
    assert len(tools) > 0
    assert any(tool["name"] == "calculator" for tool in tools)


def test_agent_reset():
    """Test agent reset functionality."""
    agent = MarketAgent()
    agent.memory.add_user_message("Test message")
    assert len(agent.memory.get_messages()) > 1  # System + user message
    
    agent.reset()
    # After reset, should only have system message
    messages = agent.memory.get_messages()
    assert len(messages) == 1
    assert messages[0]["role"] == "system"


def test_agent_chat():
    """Test agent chat functionality."""
    # This test requires a valid API key
    # Mock the response or skip if no API key
    pytest.skip("Requires valid API key")
