"""Tests for tools module."""

import pytest
from src.tools import CalculatorTool, WebScraperTool, ToolsRegistry


def test_calculator_basic_operations():
    """Test calculator basic operations."""
    calc = CalculatorTool()
    
    result = calc.basic_operation(5, 3, '+')
    assert result["status"] == "success"
    assert result["result"] == 8
    
    result = calc.basic_operation(10, 2, '/')
    assert result["status"] == "success"
    assert result["result"] == 5


def test_calculator_expression():
    """Test calculator expression evaluation."""
    calc = CalculatorTool()
    
    result = calc.calculate("2 + 2 * 3")
    assert result["status"] == "success"
    assert result["result"] == 8


def test_web_scraper_initialization():
    """Test web scraper initialization."""
    scraper = WebScraperTool()
    assert scraper is not None
    assert scraper.session is not None


def test_tools_registry():
    """Test tools registry."""
    registry = ToolsRegistry()
    
    tools = registry.list_tools()
    assert "calculator" in tools
    assert "web_scraper" in tools
    
    # Test calculator execution
    result = registry.execute_tool("calculator", {"expression": "5 + 5"})
    assert result["status"] == "success"
    assert result["result"] == 10
