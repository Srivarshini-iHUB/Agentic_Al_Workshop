# 🤖 Smart Content Creation: Agentic AI Content Refinement

A Streamlit app simulating a collaborative conversation between a Content Creator Agent and a Content Critic Agent, powered by Google Gemini LLM and Autogen. The system iteratively drafts, critiques, and refines markdown content on user-specified topics.

---

## 🗂 Folder Structure

```
.
├── app.py                # Main Streamlit app
├── README.md             # This file
├── requirements.txt      # Python dependencies
```

---

## ⚙️ Setup Instructions

### 1. 🔑 API Key Configuration

The app uses a hardcoded API key for Google Gemini API in the current code. For security, it is recommended to use environment variables or a `.env` file to store your API key securely.

---

### 2. 📦 Install Dependencies

Install required Python packages:

```bash
pip install -r requirements.txt
```

Sample `requirements.txt` should include:

```txt
streamlit
google-generativeai
autogen
langchain-google-genai
```

---

### 3. 🏁 Run the Application

Start the Streamlit app:

```bash
streamlit run app.py
```

---

## 💡 Features

* 🎯 Input a discussion topic for content creation
* 🔁 Configure number of conversation turns between Creator and Critic agents
* ✍️ Creator Agent drafts and revises markdown content
* 🧐 Critic Agent evaluates content for accuracy, clarity, and depth
* 🧠 Iterative multi-agent collaboration powered by Gemini LLM
* 🌐 Interactive Streamlit UI displaying prompts, generated content, feedback, and conversation history

---

## 🤖 Agent Descriptions

- **Content Creator Agent**: Drafts clear, concise, and technically accurate markdown content on the given topic. Revises content based on Critic feedback.
- **Content Critic Agent**: Evaluates the Creator's content for technical accuracy, clarity, depth, and provides constructive feedback.

---

## 🛠️ Usage Instructions

1. Enter a discussion topic in the input box.
2. Select the number of conversation turns (3 to 5).
3. Click the "Start Simulation" button.
4. Watch the conversation unfold turn-by-turn between Creator and Critic agents.
5. Review the final refined content and full conversation history.

---

## ⚠️ Troubleshooting

* **API Key Issues**: Ensure your Google Gemini API key is valid and properly configured.
* **Dependency Errors**: Verify all required packages are installed.
* **Performance**: The app depends on external API calls; ensure stable internet connection.

---

## 🧪 Future Improvements

* Secure API key management via environment variables
* Support for more conversation turns and agent roles
* Enhanced UI with real-time updates and export options
* Integration with other content generation and editing tools

---

## 📄 License

This project is licensed under the MIT License.
