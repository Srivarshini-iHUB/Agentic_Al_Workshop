from langchain.chains import RetrievalQA
from utils.gemini_chain import get_gemini_model
from tools.rag_tools import get_rag_retriever

def get_session_alignment_chain(event_doc_path):
    retriever = get_rag_retriever(event_doc_path)
    llm = get_gemini_model()
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
