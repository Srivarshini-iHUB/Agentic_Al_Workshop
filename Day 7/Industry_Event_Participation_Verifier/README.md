# Industry Event Participation Verifier

## Overview
The Industry Event Participation Verifier is a Streamlit-based application designed to verify participation in industry events and extract key learning outcomes. It leverages Retrieval-Augmented Generation (RAG) techniques using official event reference documents to validate evidence such as ticket PDFs, LinkedIn screenshots, and user notes.

This project was developed as part of Day 7 of the workshop.

## Features
- Upload multiple evidence files (e.g., ticket PDFs, LinkedIn screenshots) to verify event participation.
- Paste learning notes or reflections to extract key learning outcomes.
- Verify participation status using RAG verification against official event documents.
- Align extracted learnings with official event sessions.
- View a final summary of verification, learnings, session alignment, and extracted evidence.

## Reference Documents
The verification process uses official event content as reference documents. For example, the included `reference_docs.txt` contains details about the Google DevFest 2025 event, including keynote speeches, sessions, workshops, and resources.

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Virtual environment tool (venv)

### Installation
1. Clone the repository or download the project files.
2. Navigate to the project directory:
   ```bash
   cd Day 7/Industry_Event_Participation_Verifier
   ```
3. Create and activate a virtual environment:
   - On Windows:
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run the Streamlit app:
   ```bash
   streamlit run main.py
   ```
2. In the web interface:
   - Upload your evidence files (ticket PDFs, LinkedIn screenshots, etc.).
   - Paste your learning notes or reflections.
   - Enter the event name (e.g., "NASSCOM DevFest").
   - Click the "Run Verification" button.
3. View the extracted evidence, participation verification status, learning outcomes, session alignment, and final summary.

## Sample Inputs and Outputs
Sample input and output images are available in the `data/input&output/` directory:
- `input.png`: Example of uploaded evidence and notes input.
- `verfications_output.png`: Example of verification results.
- `finalSummary_output.png`: Example of the final summary output.

## Project Structure
- `main.py`: Streamlit app entry point.
- `agents/`: Contains modules for evidence extraction, participation verification, learning outcome extraction, and session alignment.
- `utils/rag_utils.py`: Utility functions for RAG verification.
- `data/reference_docs.txt`: Official event content used for verification.
- `data/sample_uploads/`: Sample evidence files for testing.

## Notes
- The project uses Retrieval-Augmented Generation (RAG) techniques to verify participation by referencing official event documents.
- Ensure the virtual environment is activated before running the app to use the correct dependencies.

Thank you for using the Industry Event Participation Verifier!
