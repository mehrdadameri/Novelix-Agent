from langchain.tools.tavily_search import TavilySearchResults

def get_tools():
    """
    Returns required tools for the agent.
    """
    # Using the built-in Tavily tool for simplicity and robustness
    search_tool = TavilySearchResults(max_results=5)
    search_tool.description = "Search the web for recent trends and articles using Tavily's Search API. Optimized for AI agents."
    return [search_tool]
