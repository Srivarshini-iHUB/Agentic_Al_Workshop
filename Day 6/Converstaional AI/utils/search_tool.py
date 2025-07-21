# utils/search_tool.py
from langchain.tools.tavily_search import TavilySearchResults
import os
from dotenv import load_dotenv
load_dotenv()

tavily = TavilySearchResults(api_key=os.getenv("TAVILY_API_KEY"))

def tavily_web_search(query):
    results = tavily.run(query)
    print(f"Search results for query '{query}': {results}")
    return results  # this is a string of search results
