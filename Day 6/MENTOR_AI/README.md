# Day 6 Mentor_AI - OKR Task Submission Classifier

## Project Description
Day 6 Mentor_AI is a Streamlit-based web application designed to classify and analyze OKR (Objectives and Key Results) task submissions. Leveraging Google's Gemini API and Langchain, the app evaluates various task types, providing insights such as priority, status, and reasons for classification. It supports multiple input formats including PDFs and web links, extracting relevant information for comprehensive task analysis.

## Features
- Supports multiple task types including:
  - Leetcode problems
  - LinkedIn Articles
  - LinkedIn Connections (PDF proof)
  - Business Cards (PDF)
  - DT Bootcamp and Gen AI Bootcamp (with proof uploads)
  - Hackathons (with proof uploads)
- Analyzes tasks to assign:
  - Priority (High, Medium, Low)
  - Status (Accepted, Rejected, Send to Mentor)
  - Reason for decision (brief explanation)
- Extracts text from PDFs for analysis using PyPDF2
- Scrapes LinkedIn articles for content analysis using BeautifulSoup
- Utilizes Langchain and Pydantic for structured output parsing
- Interactive task submission form with task-specific fields

## Installation

### Prerequisites
- Python 3.8 or higher

### Install dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Running the app
From the `Day 6/MENTOR_AI` directory, run:
```bash
streamlit run app.py
```

### Submitting tasks
- Select the task type from the dropdown.
- Fill in the required fields including title, description, and deadline.
- Provide task-specific details such as problem counts, article links, or upload PDFs as proof.
- Click "Submit Task" to analyze the submission.
- View the classification results including priority, status, and reason.

## File Structure
```
Day 6/MENTOR_AI/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── task_form.py            # Streamlit form for task submission
├── okr_tasks.json          # JSON file to save task analysis results
├── src/
│   ├── analysis/           # Task analysis logic
│   │   └── task_analyzer.py
│   ├── config/             # Configuration files
│   │   └── settings.py
│   ├── forms/              # Form related modules
│   │   └── task_form.py
│   ├── models/             # Data models for task analysis
│   │   └── task_analysis.py
│   └── utils/              # Utility functions
│       └── file_handler.py
└── data/                   # Data files such as okr_tasks.json
```

## Dependencies
- streamlit
- google-generativeai
- langchain
- langchain-google-genai
- pydantic
- PyPDF2
- beautifulsoup4
- requests

## Running the App
To start the application, run the following command in the terminal:
```bash
streamlit run app.py
```

---

This project provides an interactive and AI-powered way to classify and analyze OKR tasks, helping mentors and teams prioritize and manage their objectives effectively.
