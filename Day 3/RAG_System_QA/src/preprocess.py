from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

PDF_FOLDER = "data"
VECTOR_DB_PATH = "vectorstore/index"


def load_documents():
    all_docs = []
    for file in os.listdir(PDF_FOLDER):
        if file.endswith(".pdf"):
            loader  = PyPDFLoader(os.path.join(PDF_FOLDER,file))
            documents = loader.load()
            all_docs.extend(documents)
    return all_docs

def get_chunked_docs():
    docs = load_documents()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
    chunked_docs = splitter.split_documents(docs)
    return chunked_docs


embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")