import pymupdf  # PyMuPDF
from langchain_core.tools import tool

@tool
def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts raw text and tables from a given PDF file.
    Use this tool when you need to read the contents of a PDF document (like an inspection report).
    """
    try:
        doc = pymupdf.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        return f"Error extracting text from PDF: {str(e)}"
