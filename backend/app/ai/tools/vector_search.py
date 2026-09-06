from langchain_core.tools import tool

@tool
def search_sops(query: str) -> str:
    """
    Queries the Qdrant vector database to retrieve past Standard Operating Procedures (SOPs) relevant to the given query.
    Use this tool when you need to reference historical procedures or guidelines.
    """
    # Mock response for the celery flow verification as Qdrant integration will be refined later
    return f"Mock SOP search result for '{query}': Ensure safety protocols are followed. Check valves A and B."
