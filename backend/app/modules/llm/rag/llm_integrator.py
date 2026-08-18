from typing import List
from langchain_core.documents import Document

def format_context_for_llm(documents: List[Document]) -> str:
    """
    Formats a list of documents (chunks) into a single string suitable for an LLM prompt.
    """
    formatted_context = ""
    for i, doc in enumerate(documents):
        formatted_context += f"Document {i+1}:\n{doc.page_content}\n\n"
    return formatted_context.strip()


def generate_rag_prompt(query: str, context: str, template: str) -> str:
    """
    Generates a RAG-specific prompt by injecting the query and context into a template.
    """
    return template.format(context=context, query=query)