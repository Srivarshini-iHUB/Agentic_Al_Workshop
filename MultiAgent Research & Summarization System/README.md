# 🧠 Multi-Agent RAG System (LangGraph + Web + RAG + LLM)

An intelligent multi-agent research and summarization system designed to provide concise, accurate, and context-aware answers by orchestrating multiple specialized agents.

This project implements an intelligent multi-agent research assistant using:

- 🔀 **LangGraph**: Orchestrate dynamic agent workflows
- 🧠 **Gemini 1.5 Flash**: Google LLM for generation and summarization
- 🔍 **DuckDuckGo Search**: Web search integration
- 📄 **RAG via FAISS**: Retrieval-augmented QA from local PDFs, DOCX, and TXT files
- 🧩 **Streamlit**: Intuitive UI with interactive elements

---

## 🖼️ LangGraph Structure

```python
with st.expander("🧩 LangGraph Structure"):
    st.graphviz_chart("""
    digraph {
        Router -> Web;
        Router -> RAG;
        Router -> LLM;
        Web -> Summarizer;
        RAG -> Summarizer;
        LLM -> Summarizer;
    }
    """)
```

This illustrates the flow:

* Query goes through the `Router` agent, which classifies the query type.
* Based on classification, the query is routed to one of three agents:
  - `Web` agent for live web search
  - `RAG` agent for retrieval-augmented generation from local documents
  - `LLM` agent for direct language model generation
* All paths converge at the `Summarizer` agent, which produces the final concise output.

---

## 🗂 Folder Structure

```
.
├── app.py                # Main Streamlit app
├── my_docs/              # Folder for local PDFs, DOCX, and TXT files
├── .env                  # Environment file containing your Gemini API key
├── README.md             # This file
└── requirements.txt      # Python dependencies
```

---

## ⚙️ Setup Instructions

### 1. 🔑 Environment Setup

Create a `.env` file in the root folder:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

> You can obtain your Gemini API key from [https://makersuite.google.com/app](https://makersuite.google.com/app)

---

### 2. 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

#### Sample `requirements.txt`:

```txt
streamlit
pdfplumber
python-docx
langchain
langgraph
faiss-cpu
duckduckgo-search
python-dotenv
google-generativeai
```

---

### 3. 🏁 Run the Application

```bash
streamlit run app.py
```

---

## 💡 Features

* 🔍 **Ask Anything**: Input a query, get routed to Web, RAG, or LLM agents
* 🧠 **Automatic Routing**: Classifies queries for best agent path
* 📄 **Document Ingestion**: Reads from local `my_docs/` folder supporting PDF, DOCX, and TXT
* 🔎 **Semantic Retrieval**: Uses FAISS with Gemini embeddings for vector search
* ✨ **Concise Summarization**: Generates final answers with Gemini LLM
* 🌐 **Live Web Search**: Provides real-time information when needed

---

## ✏️ Sample Queries

* What is LangGraph?
* Summarize my document on AI safety.
* What's the latest in generative AI?
* Find points from the uploaded PDF on machine learning.

---

## 🔍 How It Works

1. **File Loader**

   * Supports `.pdf`, `.docx`, and `.txt` formats
   * Loads and splits documents into chunks using LangChain's `RecursiveCharacterTextSplitter`

2. **Vector Store (FAISS)**

   * Embeds content using Gemini Embeddings (`models/embedding-001`)
   * Enables semantic search with `retriever.as_retriever()`

3. **LangGraph Workflow**

   * `Router` agent determines query type
   * Three specialized agents handle queries:
     - `web_agent`: performs live web search
     - `rag_agent`: retrieves from local documents
     - `llm_agent`: generates answers directly from LLM
   * `summarizer_agent` consolidates and summarizes results

4. **Streamlit Interface**

   * User inputs query via UI
   * Results and LangGraph workflow visualization displayed interactively

---

## ⚠️ Troubleshooting

* **API Key Not Found**: Ensure `.env` exists and key is valid.
* **No Documents Loaded**: Make sure `my_docs/` contains valid PDF, DOCX, or TXT files.
* **Web Search Errors**: Check internet connection and `duckduckgo-search` installation.

---

## 🧪 Future Improvements

* Memory and follow-up questions (conversation state)
* File upload UI inside Streamlit
* PDF OCR (scanned documents)
* Chat-style interface

---

## 🛠️ Usage Tips

* Place your documents in the `my_docs/` folder before running the app.
* Use clear and specific queries for best results.
* Monitor console logs for debugging information.

---

## 📄 License

This project is licensed under the MIT License.
