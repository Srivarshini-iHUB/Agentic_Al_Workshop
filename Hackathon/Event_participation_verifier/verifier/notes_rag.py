from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
import os
from dotenv import load_dotenv

load_dotenv()  # This loads GOOGLE_API_KEY from .env

def setup_rag(raw_text):
    # Split text into manageable chunks
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents([Document(page_content=raw_text)])

    # Supported Gemini embedding model
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # Build FAISS vector DB
    db = FAISS.from_documents(docs, embeddings)

    # ✅ Use a supported chat model like chat-bison-001
    llm = ChatGoogleGenerativeAI(model="models/chat-bison@001", temperature=0.2)

    # Set up RetrievalQA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=db.as_retriever()
    )
    return qa_chain

def evaluate_alignment(qa_chain, student_notes):
    return qa_chain.run(student_notes)
