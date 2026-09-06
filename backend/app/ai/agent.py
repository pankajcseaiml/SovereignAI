from langgraph.prebuilt import create_react_agent
from app.ai.llm import get_llm
from app.ai.tools.document_extractor import extract_text_from_pdf
from app.ai.tools.vector_search import search_sops

def get_agent_executor():
    """
    Initializes and returns the LangGraph ReAct agent equipped with specialized industrial tools.
    """
    llm = get_llm()
    
    tools = [extract_text_from_pdf, search_sops]
    
    agent_executor = create_react_agent(llm, tools)
    
    return agent_executor
