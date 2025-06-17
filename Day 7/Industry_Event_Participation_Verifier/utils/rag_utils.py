import os
from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from PyPDF2 import PdfReader

def load_docs_from_folder(folder_path="./data"):
    all_text = ""
    for filename in os.listdir(folder_path):
        path = os.path.join(folder_path, filename)
        if filename.endswith(".pdf"):
            pdf = PdfReader(path)
            for page in pdf.pages:
                all_text += page.extract_text() or ""
        elif filename.endswith(".txt"):
            with open(path, "r", encoding="utf-8") as f:
                all_text += f.read() + "\n"
    return all_text

def split_text_to_documents(text, chunk_size=1000, chunk_overlap=100):
    splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_text(text)
    return [Document(page_content=chunk) for chunk in chunks]

def create_vectorstore_from_pdf(folder_path="./data"):
    raw_text = load_docs_from_folder(folder_path)
    docs = split_text_to_documents(raw_text)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore
