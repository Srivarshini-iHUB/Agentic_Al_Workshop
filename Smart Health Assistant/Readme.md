# 🤖 Smart Health Assistant: Personalized Health Plan Generator

A Streamlit app that leverages multi-agent collaboration powered by Google Gemini API and Autogen to generate personalized health plans including BMI calculation, diet planning, and workout scheduling based on user inputs.

---

## 🗂 Folder Structure

```
.
├── healthAgent.py        # Main Streamlit app
├── README.md             # This file
├── requirements.txt      # Python dependencies
```

---

## ⚙️ Setup Instructions

### 1. 🔑 API Key Configuration

Enter your Gemini 1.5 Flash API key in the app sidebar. You can obtain your API key from [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey).

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
```

---

### 3. 🏁 Run the Application

Start the Streamlit app:

```bash
streamlit run healthAgent.py
```

---

## 💡 Features

* 🏋️‍♂️ Calculates BMI and categorizes health status
* 🍽️ Generates personalized daily meal plans based on dietary preferences
* 🏃‍♀️ Creates 7-day workout schedules tailored to age, gender, and BMI
* 🤖 Multi-agent collaboration using Autogen and Gemini API
* 🌐 Interactive Streamlit UI with input forms and expandable agent conversation views
* 💾 Downloadable personalized health plan

---

## 🤖 Agent Descriptions

- **BMI Agent**: Calculates BMI from weight and height, categorizes it, and provides recommendations.
- **Diet Planner**: Creates meal plans based on BMI feedback and dietary preferences.
- **Workout Scheduler**: Designs workout plans considering age, gender, BMI, and diet.
- **User Proxy Agent**: Coordinates communication between user inputs and expert agents.

---

## 🛠️ Usage Instructions

1. Enter your Gemini API key in the sidebar.
2. Fill in your weight, height, age, gender, and dietary preference.
3. Click "Generate Health Plan".
4. View the generated health plan and agent conversation outputs.
5. Download the personalized health plan as a text file.

---

## ⚠️ Troubleshooting

* **API Key Issues**: Ensure your Gemini API key is valid and correctly entered.
* **Input Validation**: Use realistic values for weight, height, and age.
* **Connectivity**: Ensure stable internet connection for API calls.

---

## 🧪 Future Improvements

* Support for additional health metrics and inputs
* Enhanced UI with progress tracking and reminders
* Integration with wearable devices and health apps
* More detailed nutrition and workout recommendations

---

## 📄 License

This project is licensed under the MIT License.
