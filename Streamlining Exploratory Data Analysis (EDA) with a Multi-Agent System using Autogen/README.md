# 📊 Streamlining Exploratory Data Analysis (EDA) with a Multi-Agent System using Autogen

An intelligent multi-agent system designed to automate and enhance exploratory data analysis (EDA) on CSV datasets using Google Gemini API and Autogen multi-agent collaboration.

---

## 🗂 Folder Structure

```
.
├── app.py                # Main Streamlit app
├── .env                  # Environment file containing your Gemini API key
├── README.md             # This file
└── requirements.txt      # Python dependencies
```

---

## ⚙️ Setup Instructions

### 1. 🔑 Environment Setup

Create a `.env` file in the root folder with your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

> Obtain your Gemini API key from [https://makersuite.google.com/app](https://makersuite.google.com/app)

---

### 2. 📦 Install Dependencies

Install required Python packages:

```bash
pip install -r requirements.txt
```

Sample `requirements.txt` should include:

```txt
streamlit
pandas
google-generativeai
autogen
python-dotenv
```

---

### 3. 🏁 Run the Application

Start the Streamlit app:

```bash
streamlit run app.py
```

---

## 💡 Features

* 📁 Upload CSV datasets for analysis
* 🧹 Automated data cleaning and preprocessing
* 📊 Exploratory data analysis with summary statistics and insights
* 📝 Automated EDA report generation
* 🧐 Critique and review of generated reports
* ✅ Validation of preprocessing code
* 🤖 Multi-agent collaboration powered by Autogen and Gemini API
* 🌐 Interactive Streamlit UI with expandable output sections

---

## 🤖 Agent Descriptions

- **DataPrepAgent**: Cleans data by handling missing values, fixing data types, and removing duplicates. Returns Python preprocessing code.
- **EDAAgent**: Provides summary statistics, extracts insights, and suggests visualizations.
- **ReportGeneratorAgent**: Creates a clean EDA report based on insights including overview, key findings, and visual suggestions.
- **CriticAgent**: Reviews the EDA report for clarity, accuracy, completeness, and suggests improvements.
- **ExecutorAgent**: Validates the data preprocessing code for correctness and suggests corrections.

---

## 🛠️ Usage Instructions

1. Upload a CSV file using the file uploader.
2. Preview the dataset in the UI.
3. Click the "Run Agentic EDA" button to start the multi-agent analysis.
4. View outputs from each agent in expandable sections:
   - Data Preparation Output (Python code)
   - EDA Insights
   - EDA Report
   - Critic Review
   - Code Validation
5. Use the insights and code for further analysis or integration.

---

## ⚠️ Troubleshooting

* **API Key Not Found**: Ensure `.env` file exists with a valid `GEMINI_API_KEY`.
* **File Upload Issues**: Only CSV files are supported.
* **Agent Errors**: Check internet connection and Gemini API status.

---

## 🧪 Future Improvements

* Support for additional file formats (Excel, JSON)
* Enhanced visualization generation and display
* Interactive report editing and export
* Integration with other data science tools and pipelines

---

## 📄 License

This project is licensed under the MIT License.
