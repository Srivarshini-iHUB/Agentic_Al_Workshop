from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from utils.rag_utils import create_vectorstore_from_pdf
import os
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def align_sessions(event_name, user_learnings):
    vectorstore = create_vectorstore_from_pdf("./data")
    retriever = vectorstore.as_retriever()

    qa = RetrievalQA.from_chain_type(
        llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash"),
        retriever=retriever,
        return_source_documents=False
    )

    query = f"Compare the user's learning notes with the official content of {event_name}. Are they aligned?\n\n{user_learnings}"
    return qa.run(query)
