from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.tools import tool
import os
from dotenv import load_dotenv

load_dotenv()  # To load TAVILY_API_KEY

@tool
def get_attractions(city: str) -> str:
    """Returns top tourist attractions in a city using Tavily Search API."""
    search = TavilySearchResults(api_key=os.getenv("TAVILY_API_KEY"))
    results = search.run(f"Top tourist attractions in {city}")
    return results

def get_attractions_tool():
    return get_attractions
