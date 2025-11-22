"""Web scraping tool for collecting market data."""

import requests
from bs4 import BeautifulSoup


def scrape_webpage(url):
    """Scrape content from a webpage.
    
    Args:
        url: The URL to scrape.
        
    Returns:
        Scraped content as a string or error message.
    """
    try:
        if not url.startswith(('http://', 'https://')):
            return "Error: Invalid URL"
        
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        response = session.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('title')
        title_text = title.get_text().strip() if title else "No title"
        
        for script in soup(["script", "style", "nav", "footer", "aside"]):
            script.decompose()
        
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        if len(text) > 3000:
            text = text[:3000] + "... [truncated]"
        
        return f"Title: {title_text}\n\nContent:\n{text}"
    
    except requests.Timeout:
        return f"Error: Timeout accessing {url}"
    except requests.RequestException as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"
