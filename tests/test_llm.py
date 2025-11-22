"""Tests for LLM module."""

import pytest
from src.llm import GroqLLM


def test_groq_llm_initialization():
    """Test Groq LLM initialization."""
    llm = GroqLLM()
    assert llm is not None
    assert llm.model is not None


def test_groq_llm_chat():
    """Test Groq LLM chat functionality."""
    # This test requires a valid API key
    # Mock the response or skip if no API key
    pytest.skip("Requires valid API key")


def test_groq_llm_generate():
    """Test Groq LLM generate functionality."""
    # This test requires a valid API key
    # Mock the response or skip if no API key
    pytest.skip("Requires valid API key")
