import requests
import os

def perform_web_search(query: str):
    """
    Perform a web search using Serper.dev API
    Returns summarized text.
    """
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        raise ValueError("SERPER_API_KEY not found in environment.")

    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "q": query
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        results = data.get('organic', [])
        if not results:
            return "No relevant search results found."

        output = ""
        for item in results[:3]:  # Top 3 results
            title = item.get('title', '')
            link = item.get('link', '')
            snippet = item.get('snippet', '')
            output += f"🔗 {title}\n{snippet}\n{link}\n\n"

        return output.strip()

    except Exception as e:
        return f"Error during web search: {str(e)}"
