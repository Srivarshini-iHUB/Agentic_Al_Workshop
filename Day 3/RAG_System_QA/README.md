# RAG System QA - AI Research Papers

## Project Description
This project implements a Retrieval-Augmented Generation (RAG) system for question answering on AI research papers. It uses a combination of vector search over document embeddings and a Google Generative AI language model to provide answers with source references from the research papers.

The system is built with LangChain, FAISS for vector search, and Streamlit for the user interface.

## Features
- Load and preprocess AI research papers in PDF format.
- Split documents into chunks and generate embeddings using HuggingFace sentence transformers.
- Store embeddings in a FAISS vectorstore for efficient similarity search.
- Use Google Generative AI (Gemini 2.0 Flash) as the language model for generating answers.
- Streamlit app for interactive question answering with source document display.

## Installation

1. Clone the repository and navigate to the project directory.

2. Install the required Python packages:
```
pip install -r requirements.txt
```

3. Set up environment variables:
- Create a `.env` file in the project root.
- Add your Google API key:
```
GOOGLE_API_KEY=your_google_api_key_here
```

## Usage

1. Place your AI research paper PDFs in the `data/` folder.

2. Run the Streamlit app:
```
streamlit run app.py
```

3. Enter your question in the input box to get answers with source references.

## Project Structure

- `app.py`: Streamlit application entry point.
- `src/pipeline.py`: Defines the retrieval QA pipeline using LangChain and Google Generative AI.
- `src/retriever.py`: Loads or creates the FAISS vectorstore from document embeddings.
- `src/preprocess.py`: Loads PDF documents, splits them into chunks, and generates embeddings.
- `data/`: Folder containing AI research paper PDFs.
- `vectorstore/index/`: Local FAISS index storage.

## Notes

- The FAISS index is automatically created if missing when running the app.
- The system uses the "gemini-2.0-flash" model from Google Generative AI.
- Document embeddings use the "sentence-transformers/all-MiniLM-L6-v2" model.

