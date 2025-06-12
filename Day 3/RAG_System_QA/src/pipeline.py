from langchain.chains import RetrievalQA
from langchain_google_genai import GoogleGenerativeAI
from .retriever import load_vectorstore

import os
from dotenv import load_dotenv
load_dotenv()

# Load LLM
llm = GoogleGenerativeAI(
    model="gemini-2.0-flash",
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.2
)

# Load retriever from vector store
vectorstore = load_vectorstore()
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# Create QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

# Define answer function
def answer_question(question):
    result = qa_chain({"query": question})
    return result['result'], result['source_documents']