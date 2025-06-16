from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Create retriever for RAG
def setup_rag(raw_text):
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents([Document(page_content=raw_text)])

    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(docs, embeddings)
    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(temperature=0.2),
        retriever=db.as_retriever()
    )
    return qa_chain

def evaluate_alignment(qa_chain, student_notes):
    return qa_chain.run(student_notes)
