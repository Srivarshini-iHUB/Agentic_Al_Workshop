# 🎓 Industry Event Participation Verifier (LangChain + Gemini)

This project is a Streamlit-based AI assistant that automates the verification of student participation in industry events using uploaded evidence (such as tickets, LinkedIn posts, and handwritten notes). It performs multi-step reasoning to extract relevant information and compares it with official session materials using Retrieval-Augmented Generation (RAG).

---

## 🚀 Features

- 📝 Upload multiple evidence files (PDF, images, LinkedIn post, notes)
- 📘 Upload official session document
- 🔍 AI-based evidence extraction using LangChain and Gemini
- ✅ Participation verification based on multi-source evidence
- 🧠 Learning outcome extraction from student notes
- 📚 RAG-based comparison with official session document
- 📊 Similarity scoring between student learnings and session content

---

## 🛠️ Project Structure

```bash
event_verifier/
│
├── agents/
│   ├── evidence_extractor.py
│   ├── participation_verifier.py
│   ├── learning_outcome_extractor.py
│   └── session_alignment_agent.py
│
├── tools/
│   ├── file_tools.py
│   └── rag_tools.py
│
├── uploads/
│   ├── inputs/       # Uploaded student files
│   └── materials/    # Uploaded session documents
│
├── main.py           # Streamlit UI
├── requirements.txt
└── README.md

📂 Input Requirements
Student Evidence Files (upload via sidebar):

.pdf, .png, .jpg, .txt

Ticket, LinkedIn post, handwritten or typed notes

Session Document:

Plain text .txt file describing the event content or agenda

📦 Installation
Clone the repo

bash
Copy
Edit
git clone https://github.com/your-org/event-verifier.git
cd event-verifier
Create and activate a virtual environment

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # on Linux/Mac
venv\Scripts\activate     # on Windows
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
❗ If you are using FAISS, make sure to install the appropriate version:

bash
Copy
Edit
pip install faiss-cpu   # Most compatible
# OR
pip install faiss-gpu   # For CUDA/GPU support
▶️ Running the App
bash
Copy
Edit
streamlit run main.py
This will open a web app in your browser.

🧠 How it Works (Processing Pipeline)
Evidence Extraction: Uses Gemini to identify relevant proofs from student uploads.

Participation Verification: Determines if the student attended the event.

Learning Outcome Extraction: Extracts learning reflections or outcomes from notes.

RAG Alignment: Compares extracted learning with official session document using vector similarity.

Similarity Score: Displays how well student learning aligns with the event’s actual agenda.

💡 Example Use Case
A faculty uploads a student’s ticket, LinkedIn post, and notes. The app processes all content, verifies if the student attended the event, extracts learning outcomes, and checks if their learnings match the official event content.

🧩 Dependencies
Streamlit

LangChain

Google Generative AI (Gemini)

FAISS or Chroma

PyMuPDF, Pillow, pytesseract for file and image handling