import os
import streamlit as st
import pdfplumber
from docx import Document as DocxDocument
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langgraph.graph import StateGraph
from langchain_core.runnables import RunnableLambda
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.tools import DuckDuckGoSearchRun

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise EnvironmentError("Missing GOOGLE_API_KEY in .env file")

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
search_tool = DuckDuckGoSearchRun()

st.set_page_config(page_title="🧠 Smart Research Companion", layout="wide")
st.title("🧠 Smart Research Companion")
st.markdown("An AI-powered assistant using Gemini + LangGraph + Web Search")

def read_text(file_path):
    if file_path.endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            return "\n".join([p.extract_text() for p in pdf.pages if p.extract_text()])
    elif file_path.endswith(".docx"):
        doc = DocxDocument(file_path)
        return "\n".join([p.text for p in doc.paragraphs])
    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return ""

doc_dir = "data"
all_texts = []
if os.path.exists(doc_dir):
    for file in os.listdir(doc_dir):
        file_path = os.path.join(doc_dir, file)
        content = read_text(file_path)
        if content:
            all_texts.append(content)

if all_texts:
    raw_docs = text_splitter.create_documents(all_texts)
    vector_db = FAISS.from_documents(raw_docs, embeddings)
    retriever = vector_db.as_retriever()
else:
    fallback = [Document(page_content="LangGraph enables custom multi-agent workflows in Python."),
                Document(page_content="Gemini 1.5 Flash is optimized for speed and multi-turn summarization.")]
    vector_db = FAISS.from_documents(fallback, embeddings)
    retriever = vector_db.as_retriever()

def classify_query(state):
    query = state["query"]
    classifier_prompt = PromptTemplate.from_template("""Classify this query: '{query}' as one of [search, documents, general]. Reply with the label only.""")
    response = (classifier_prompt | llm).invoke({"query": query}).content.lower()
    if "search" in response:
        return {**state, "route": "search"}
    elif "document" in response:
        return {**state, "route": "documents"}
    else:
        return {**state, "route": "general"}

def web_search_agent(state):
    try:
        result = search_tool.run(state["query"])
        return {**state, "content": result}
    except Exception as err:
        return {**state, "content": f"Error during web search: {err}"}

def document_agent(state):
    chain = RetrievalQA.from_chain_type(llm=llm, retriever=state["retriever"])
    answer = chain.run(state["query"])
    return {**state, "content": answer}

def general_llm_agent(state):
    result = llm.invoke(state["query"])
    return {**state, "content": result.content}

def summarize_output(state):
    summary_prompt = PromptTemplate.from_template("""Summarize the following answer:

{content}

Provide a brief overview.""")
    summary = (summary_prompt | llm).invoke({"content": state["content"]})
    return {**state, "summary": summary.content}

def process_query(query_text, retriever):
    graph = StateGraph(dict)
    graph.set_entry_point("router")

    graph.add_node("router", RunnableLambda(classify_query))
    graph.add_node("search", RunnableLambda(web_search_agent))
    graph.add_node("documents", RunnableLambda(document_agent))
    graph.add_node("general", RunnableLambda(general_llm_agent))
    graph.add_node("summarizer", RunnableLambda(summarize_output))

    graph.add_conditional_edges("router", lambda state: state["route"], {
        "search": "search",
        "documents": "documents",
        "general": "general"
    })

    for node in ["search", "documents", "general"]:
        graph.add_edge(node, "summarizer")

    graph.set_finish_point("summarizer")
    return graph.compile().invoke({"query": query_text, "retriever": retriever})

st.markdown("### Ask a question:")
user_input = st.text_input("", placeholder="What is Gemini 1.5 used for?", label_visibility="collapsed")

if st.button("Get Answer"):
    if not user_input.strip():
        st.warning("Please enter a valid query.")
    else:
        with st.spinner("Processing your question..."):
            result = process_query(user_input, retriever)
            st.success("Answer ready!")
            st.markdown("#### Answer")
            st.write(result.get("content", "No content found."))
            st.markdown("#### Summary")
            st.write(result.get("summary", "No summary available."))
