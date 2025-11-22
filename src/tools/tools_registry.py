"""Simple tools registry - exports available tools"""

from typing import List, Dict


def get_tools_info() -> List[Dict]:
    """Get information about available tools.
    
    Returns:
        List of tool information dictionaries.
    """
    return [
        {
            "name": "Calculator",
            "description": "Perform mathematical calculations"
        },
        {
            "name": "WebScraper",
            "description": "Scrape content from web pages"
        },
        {
            "name": "SearchKnowledge",
            "description": "Search the knowledge base"
        }
    ]
