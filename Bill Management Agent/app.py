import os
import json
import tempfile
import streamlit as st
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as gemini_sdk
from autogen.agentchat import UserProxyAgent, AssistantAgent, GroupChat, GroupChatManager

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
gemini_sdk.configure(api_key=API_KEY)
gemini = gemini_sdk.GenerativeModel("models/gemini-1.5-flash")

st.set_page_config(
    page_title="📃 Smart Expense Analyzer",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    #MainMenu, footer, header {visibility: hidden;}
    .header { text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea, #764ba2); color: white; border-radius: 16px; margin-bottom: 2rem; }
    .header h1 { font-size: 2.4rem; font-weight: 700; margin-bottom: 0.5rem; }
    .header p { font-size: 1.1rem; margin: 0; opacity: 0.9; }
    .upload-box { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 2rem; border-radius: 16px; text-align: center; margin-bottom: 2rem; }
    .upload-box h3 { color: white; font-weight: 600; margin-bottom: 1rem; }
    .category-block { background: white; padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem; border-left: 4px solid #667eea; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    .category-title { font-weight: 600; font-size: 1.2rem; margin-bottom: 1rem; display: flex; justify-content: space-between; align-items: center; }
    .expense-entry { display: flex; justify-content: space-between; padding: 0.7rem 1rem; border-radius: 8px; background: #f8fafc; margin-bottom: 0.5rem; border-left: 3px solid #38b2ac; }
    .stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin: 2rem 0; }
    .stat-box { background: white; border-top: 4px solid #38b2ac; text-align: center; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
    .stat-value { font-size: 2rem; font-weight: bold; color: #667eea; }
    .stat-label { font-size: 0.9rem; color: #718096; margin-top: 0.5rem; }
    .ai-summary { background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 2rem; border-radius: 15px; margin: 2rem 0; }
    .chat-log { background: #f8fafc; padding: 2rem; border-radius: 15px; margin-top: 2rem; }
    .message { margin: 1rem 0; padding: 1rem 1.5rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
    .from-user { background: linear-gradient(135deg, #667eea, #764ba2); color: white; margin-left: 2rem; }
    .from-agent { background: white; color: #2d3748; margin-right: 2rem; border-left: 4px solid #38b2ac; }
    .msg-sender { font-weight: 600; font-size: 0.9rem; opacity: 0.8; margin-bottom: 0.5rem; }
    .msg-body { font-size: 1rem; line-height: 1.5; }
    .success { background: linear-gradient(135deg, #48bb78, #38a169); color: white; padding: 1rem; border-radius: 10px; margin: 1rem 0; font-weight: 500; }
    .error { background: linear-gradient(135deg, #f56565, #e53e3e); color: white; padding: 1rem; border-radius: 10px; margin: 1rem 0; font-weight: 500; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="header">
        <h1>📃 Smart Expense Analyzer</h1>
        <p>Let AI break down your expenses intelligently from a bill image</p>
    </div>
""", unsafe_allow_html=True)

middle_column = st.columns([1, 2, 1])[1]
with middle_column:
    st.markdown('<div class="upload-box"><h3>🖼 Upload Bill Image</h3></div>', unsafe_allow_html=True)
    bill_image = st.file_uploader("", type=["jpg", "jpeg", "png"], help="Only JPG, JPEG, PNG files allowed")

if 'interaction_log' not in st.session_state:
    st.session_state.interaction_log = []

EXPENSE_ICONS = {
    "Groceries": "🛒", "Dining": "🍽️", "Utilities": "⚡", "Shopping": "🛍️",
    "Entertainment": "🎬", "Transportation": "🚗", "Healthcare": "🏥",
    "Education": "📚", "Others": "📦"
}

def extract_expenses_from_image(image_file):
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(image_file.read())
            img_path = tmp.name

        image = Image.open(img_path)
        query = """
        Extract all expenses from this bill image. Group them into categories: 
        Groceries, Dining, Utilities, Shopping, Entertainment, Transportation, Healthcare, Education, Others. 
        Return as JSON format like {"category": [{"item": "item_name", "cost": "amount"}]}.
        Make sure the cost is just the number without currency symbol.
        """

        result = gemini.generate_content([query, image])
        response_text = result.text.strip()
        json_start = response_text.find("{")
        json_end = response_text.rfind("}") + 1

        if json_start != -1 and json_end != -1:
            return json.loads(response_text[json_start:json_end]), response_text
        else:
            return None, response_text
    except Exception as err:
        st.error(f"Failed to extract: {err}")
        return None, str(err)
    finally:
        if 'img_path' in locals():
            os.unlink(img_path)

def generate_expense_summary(data):
    try:
        analysis_prompt = f"""
        Analyze the following categorized expenses: {data}
        Provide a summary that includes:
        1. Total expenditure
        2. Totals per category
        3. Highest category and possible reasons
        4. Any outliers or odd patterns
        5. Brief money-saving tips
        """
        summary = gemini.generate_content(analysis_prompt)
        return summary.text.strip()
    except Exception as e:
        return f"Summary Error: {str(e)}"

def compute_statistics(parsed_data):
    total = 0
    category_sums = {}
    count = 0

    for cat, items in parsed_data.items():
        subtotal = 0
        for item in items:
            try:
                amount = float(str(item['cost']).replace('₹', '').replace(',', ''))
                subtotal += amount
                count += 1
            except Exception:
                continue
        if subtotal > 0:
            category_sums[cat] = subtotal
            total += subtotal

    return {
        "total": total,
        "categories": category_sums,
        "items": count,
        "category_count": len(category_sums)
    }

user = UserProxyAgent(name="UserAgent", human_input_mode="NEVER", code_execution_config={"use_docker": False}, llm_config=False)
processor = AssistantAgent(name="ProcessorAgent", system_message="Categorize expenses into structured data.", llm_config=False)
analyzer = AssistantAgent(name="SummaryAgent", system_message="Analyze categorized expenses and give insights.", llm_config=False)
group = GroupChat(agents=[user, processor, analyzer])
coordinator = GroupChatManager(groupchat=group)

if bill_image:
    st.markdown('<div class="success">✅ Bill uploaded successfully. Processing...</div>', unsafe_allow_html=True)
    st.image(bill_image, caption="Uploaded Bill", use_column_width=True)

    with st.spinner("📂 Extracting details..."):
        parsed, raw = extract_expenses_from_image(bill_image)

    if not parsed:
        st.markdown('<div class="error">❌ Failed to extract data from bill.</div>', unsafe_allow_html=True)
        with st.expander("View raw Gemini output"):
            st.text(raw)
    else:
        stats = compute_statistics(parsed)
        st.session_state.interaction_log.clear()

        user.send("Bill uploaded", coordinator)
        st.session_state.interaction_log.append(("UserAgent → GroupManager", "Bill uploaded"))

        user.send(f"Categorized data: {parsed}", processor)
        st.session_state.interaction_log.append(("UserAgent → ProcessorAgent", json.dumps(parsed, indent=2)))
        st.session_state.interaction_log.append(("ProcessorAgent", f"Categorized {stats['items']} items into {stats['category_count']} groups."))

        user.send("Analyze categorized expenses", analyzer)
        st.session_state.interaction_log.append(("UserAgent → SummaryAgent", "Analyze categorized expenses"))

        with st.spinner("💡 Generating insights..."):
            summary = generate_expense_summary(parsed)
        st.session_state.interaction_log.append(("SummaryAgent", summary))

        # Display statistics
        st.markdown(f"""
            <div class="stat-grid">
                <div class="stat-box"><div class="stat-value">₹{stats['total']:,.2f}</div><div class="stat-label">Total Spent</div></div>
                <div class="stat-box"><div class="stat-value">{stats['items']}</div><div class="stat-label">Items</div></div>
                <div class="stat-box"><div class="stat-value">{stats['category_count']}</div><div class="stat-label">Categories</div></div>
                <div class="stat-box"><div class="stat-value">₹{stats['total']/stats['items']:,.2f}</div><div class="stat-label">Avg/Item</div></div>
            </div>
        """, unsafe_allow_html=True)

        # Expense breakdown
        st.markdown("## 🗂 Categorized Expenses")
        for cat, items in {k: v for k, v in parsed.items() if v}.items():
            cat_sum = sum(float(str(x['cost']).replace('₹', '').replace(',', '')) for x in items if 'cost' in x)
            st.markdown(f"""
                <div class="category-block">
                    <div class="category-title">{EXPENSE_ICONS.get(cat, '📦')} {cat} <span style="color:#38b2ac;">₹{cat_sum:,.2f}</span></div>
            """, unsafe_allow_html=True)
            for entry in items:
                if 'item' in entry and 'cost' in entry:
                    st.markdown(f"""
                        <div class="expense-entry">
                            <span>{entry['item']}</span><span>₹{entry['cost']}</span>
                        </div>
                    """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Summary
        st.markdown(f"""
            <div class="ai-summary">
                <h2>📈 Summary & Recommendations</h2>
                <div style="font-size: 1.1rem;">{summary}</div>
            </div>
        """, unsafe_allow_html=True)

        # Logs
        st.markdown('<div class="chat-log"><h2>🧠 Agent Communication Logs</h2>', unsafe_allow_html=True)
        for sender, msg in st.session_state.interaction_log:
            style = "from-user" if "UserAgent" in sender else "from-agent"
            st.markdown(f"""
                <div class="message {style}">
                    <div class="msg-sender">{sender}</div>
                    <div class="msg-body">{msg}</div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.markdown("""
        <div style="text-align: center; padding: 3rem; color: #718096;">
            <h3>📥 Upload a bill image to begin</h3>
            <p>AI will read and break down your expenses with actionable insights</p>
        </div>
    """, unsafe_allow_html=True)
