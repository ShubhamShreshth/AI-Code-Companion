from mcp.server.fastmcp import FastMCP
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import json
from typing import List, Dict, Optional

# MCP server
mcp = FastMCP("Google Search MCP")

class GoogleSearchMCP:
    def __init__(self):
        self.search_results_cache = {}
    
    def search_google(self, query: str, num_results: int = 10) -> List[Dict]:
        """
        Search Google and return results with titles, URLs, and snippets
        """
        try:
            results = []
            search_results = search(query, num_results=num_results, lang="en")
            
            for i, url in enumerate(search_results):
                result = {
                    "title": f"Result {i+1}",
                    "url": url,
                    "snippet": f"Search result for: {query}"
                }
                
                # Try to get page title and snippet
                try:
                    response = requests.get(url, timeout=5, headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    })
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Get title
                    title_tag = soup.find('title')
                    if title_tag:
                        result["title"] = title_tag.get_text().strip()
                    
                    # Get meta description
                    meta_desc = soup.find('meta', attrs={'name': 'description'})
                    if meta_desc:
                        result["snippet"] = meta_desc.get('content', '')[:200] + "..."
                    else:
                        # Fallback to first paragraph
                        first_p = soup.find('p')
                        if first_p:
                            result["snippet"] = first_p.get_text().strip()[:200] + "..."
                            
                except Exception as e:
                    # If we can't fetch the page, keep the default values
                    pass
                
                results.append(result)
            
            return results
            
        except Exception as e:
            return [{"error": f"Search failed: {str(e)}"}]

# Initialize the search handler
search_handler = GoogleSearchMCP()

@mcp.tool()
def google_search(query: str, num_results: int = 5) -> str:
    """
    Search Google for the given query and return results
    """
    results = search_handler.search_google(query, num_results)
    
    if results and "error" in results[0]:
        return results[0]["error"]
    
    formatted_results = []
    for i, result in enumerate(results, 1):
        formatted_results.append(
            f"{i}. {result['title']}\n"
            f"   URL: {result['url']}\n"
            f"   {result['snippet']}\n"
        )
    
    return f"Search results for '{query}':\n\n" + "\n".join(formatted_results)

@mcp.tool()
def search_and_summarize(query: str, num_results: int = 3) -> str:
    """
    Search Google and provide a summary of the top results
    """
    results = search_handler.search_google(query, num_results)
    
    if results and "error" in results[0]:
        return results[0]["error"]
    
    summary = f"Summary of top {len(results)} results for '{query}':\n\n"
    
    for i, result in enumerate(results, 1):
        summary += f"{i}. {result['title']}\n"
        summary += f"   {result['snippet']}\n\n"
    
    return summary

@mcp.tool()
def search_with_filters(query: str, site_filter: Optional[str] = None, num_results: int = 5) -> str:
    """
    Search Google with optional site filter
    """
    if site_filter:
        search_query = f"{query} site:{site_filter}"
    else:
        search_query = query
    
    results = search_handler.search_google(search_query, num_results)
    
    if results and "error" in results[0]:
        return results[0]["error"]
    
    formatted_results = []
    for i, result in enumerate(results, 1):
        formatted_results.append(
            f"{i}. {result['title']}\n"
            f"   URL: {result['url']}\n"
            f"   {result['snippet']}\n"
        )
    
    filter_info = f" (filtered to {site_filter})" if site_filter else ""
    return f"Search results for '{query}'{filter_info}:\n\n" + "\n".join(formatted_results)

# Resource to get the latest search results
@mcp.resource("google://search/{query}")
def get_search_resource(query: str) -> str:
    """
    Resource endpoint for Google search results
    """
    results = search_handler.search_google(query, 3)
    
    if results and "error" in results[0]:
        return results[0]["error"]
    
    formatted_results = []
    for i, result in enumerate(results, 1):
        formatted_results.append(
            f"{i}. {result['title']}\n"
            f"   URL: {result['url']}\n"
            f"   {result['snippet']}\n"
        )
    
    return f"Latest search results for '{query}':\n\n" + "\n".join(formatted_results)

# Prompt template for search assistance
@mcp.prompt()
def search_assistant_prompt() -> str:
    """
    Prompt template for Google search assistance
    """
    return """You are a Google Search Assistant. You can help users find information by searching Google.

                Available tools:
                - google_search: Search Google and return detailed results with titles, URLs, and snippets
                - get_search_links: Get just the links from a Google search
                - search_and_summarize: Search and provide a summary of top results
                - search_with_filters: Search with optional site filters

                To help users, you can:
                1. Search for general information
                2. Find specific websites or resources
                3. Get links to relevant content
                4. Summarize search results
                5. Filter searches to specific domains

                Just ask what the user wants to search for and I'll help you find the information!"""
