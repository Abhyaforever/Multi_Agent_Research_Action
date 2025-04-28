# Web Search Tool
import requests
import json
import os
from typing import List, Dict

def perform_web_search(query: str) -> List[Dict]:
    """
    Performs a web search using the DuckDuckGo API
    Returns a list of search results with title, link, and snippet
    """
    # Basic validation: skip if query looks like HTML or CSS
    if any(x in query.lower() for x in ["<html", "<head", "<body", "<style", ":root", "--bprogress"]):
        print(f"Web search skipped for invalid query: {query[:60]}...")
        return [{'title': 'Invalid Query', 'snippet': 'Query looked like HTML/CSS and was skipped.', 'link': None}]
    try:
        # Using DuckDuckGo API
        url = f"https://api.duckduckgo.com/?q={query}&format=json"
        response = requests.get(url, timeout=3)
        data = response.json()
        results = []
        if 'RelatedTopics' in data:
            for topic in data['RelatedTopics'][:5]:  # Get top 5 results
                if 'Text' in topic and 'FirstURL' in topic:
                    results.append({
                        'title': topic['Text'].split(' - ')[0],
                        'snippet': topic['Text'],
                        'link': topic['FirstURL']
                    })
        # If no results, return a fallback
        if not results:
            return [{'title': 'No Results', 'snippet': 'No web results found or API returned nothing.', 'link': None}]
        return results
    except Exception as e:
        print(f"Error in web search: {str(e)}")
        return [{'title': 'Web Search Unavailable', 'snippet': f'Web search timed out or failed: {str(e)}. Continuing without web results.', 'link': None}]
