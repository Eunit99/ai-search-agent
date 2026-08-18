import os
import requests
from dotenv import load_dotenv

# Load API keys from environment variables
load_dotenv()
SEARCHAPI_KEY = os.getenv("SEARCHAPI_API_KEY")

def search_web(query: str, location: str = "United States") -> str:
    """
    Queries the SearchApi.io Google Search engine and returns a compressed
    string containing the titles, snippets, and links of organic results.
    """
    if not SEARCHAPI_KEY:
        return "Error: SearchApi API key missing from environment variables."

    url = "https://www.searchapi.io/api/v1/search"

    params = {
        "engine": "google",
        "q": query,
        "location": location,
        "api_key": SEARCHAPI_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        organic_results = data.get("organic_results", [])
        if not organic_results:
            return f"No relevant web search results found for: '{query}'"

        formatted_results = []
        for index, result in enumerate(organic_results[:5], 1):
            title = result.get("title", "No Title")
            snippet = result.get("snippet", "No Snippet Available")
            link = result.get("link", "")
            if len(snippet) > 40:
                formatted_results.append(f"[{index}] {title}\nSnippet: {snippet}\nSource: {link}\n---")

        return "\n".join(formatted_results)

    except requests.exceptions.RequestException as e:
        return f"An infrastructure error occurred while querying the search API: {str(e)}"


if __name__ == "__main__":
    test_query = "Who won the men's 100m sprint in the 2024 Paris Olympics?"
    print(f"Testing SearchApi wrapper with query: '{test_query}'...\n")
    print(search_web(test_query))
