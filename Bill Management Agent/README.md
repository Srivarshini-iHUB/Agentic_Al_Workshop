# 💼 AI Bill Management Agent

An AI-powered Streamlit application that allows users to upload bill images and automatically categorizes expenses into predefined categories using Google Gemini AI. The app provides detailed expense summaries, intelligent insights, and displays agent communication logs for transparency.

## 🚀 Features

- Upload bill images (JPG, JPEG, PNG) for processing
- AI-driven extraction and categorization of expenses into categories such as Groceries, Dining, Utilities, Shopping, Entertainment, Transportation, Healthcare, Education, and Others
- Calculation of total expenditure, category-wise totals, item counts, and average spending per item
- AI-generated comprehensive spending analysis with financial insights and recommendations
- Interactive display of categorized expenses with icons and totals
- Agent communication logs showing the interaction between user proxy and AI agents
- Clean, responsive UI with enhanced CSS styling for better user experience

## 🧰 Requirements

- Python 3.8+
- Streamlit
- Google Gemini API key

## 📦 Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd Bill Management Agent
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:

Create a `.env` file in the project root with your Google Gemini API key:

```
GEMINI_API_KEY=your_api_key_here
```

## 🚀 Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

Upload a bill image in JPG, JPEG, or PNG format. The app will process the image, categorize expenses, and display a detailed summary along with AI-generated insights.

## 🛠️ Technologies Used

- [Streamlit](https://streamlit.io/) for the web interface
- [Google Gemini AI](https://developers.generativeai.google/) for expense extraction and summarization
- AutoGen agents for managing AI interactions and processing
- Python libraries: `PIL` for image processing, `dotenv` for environment variables

---


