import os
import json
import tempfile
import streamlit as st
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai
from autogen.agentchat import UserProxyAgent, AssistantAgent, GroupChat, GroupChatManager

# --- Environment Setup ---
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
vision_model = genai.GenerativeModel("models/gemini-1.5-flash")

# --- Streamlit Layout Config ---
st.set_page_config(
    page_title="🧾 Smart Bill Insight",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Global State Setup ---
if "chat_logs" not in st.session_state:
    st.session_state.chat_logs = []

# --- Custom Styles ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    #MainMenu, footer, header {visibility: hidden;}
    .app-header {
        background: linear-gradient(120deg, #667eea, #764ba2);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .upload-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        text-align: center;
        border-radius: 12px;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
    <div class="app-header">
        <h1>🧾 Smart Bill Insight Agent</h1>
        <p>Instantly analyze your receipts using Generative AI</p>
    </div>
""", unsafe_allow_html=True)

# --- File Upload Section ---
col_center = st.columns([1, 2, 1])[1]
with col_center:
    st.markdown('<div class="upload-box"><h3>📤 Upload Your Receipt</h3></div>', unsafe_allow_html=True)
    uploaded_image = st.file_uploader("", type=["jpg", "jpeg", "png"])

# --- Category Emojis ---
CATEGORY_ICONS = {
    "Groceries": "🛒",
    "Dining": "🍽️",
    "Utilities": "⚡",
    "Shopping": "🛍️",
    "Entertainment": "🎬",
    "Transportation": "🚗",
    "Healthcare": "🏥",
    "Education": "📚",
    "Others": "📦"
}

# --- Gemini JSON Parsing ---
def extract_expenses(image: Image.Image) -> list:
    prompt = """
You are a receipt analyzer. The uploaded image is a photo of a bill or purchase receipt.
Your job is to extract the following details from the image:
- Store/Vendor Name
- Date of Transaction
- List of Items with:
  - Name
  - Price
  - Quantity (if available)
- Total Amount
- Applicable Taxes (optional)
- Payment Method (optional)

Output must strictly follow this JSON format:
{
  "store_name": "string",
  "transaction_date": "YYYY-MM-DD",
  "items": [
    {"name": "item_name", "price": float, "quantity": int (optional)},
    ...
  ],
  "total_amount": float,
  "taxes": float (optional),
  "payment_method": "string" (optional)
}
"""
    gemini_response = vision_model.generate_content([prompt, image])
    text_response = gemini_response.text
    try:
        json_start = text_response.find("{")
        json_data = json.loads(text_response[json_start:])
        return json_data
    except Exception as e:
        st.error("❌ Could not parse receipt data. Please try a clearer image.")
        return None

# --- Expense Categorization ---
def tag_expense(item_name: str) -> str:
    query = f"""
Classify the following item into a spending category. Choose from:
['Groceries', 'Dining', 'Utilities', 'Shopping', 'Entertainment', 'Transportation', 'Healthcare', 'Education', 'Others']
Item: "{item_name}"
Only respond with the category name.
"""
    response = vision_model.generate_content(query)
    return response.text.strip()

# --- Upload & Processing ---
if uploaded_image:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
        tmp_file.write(uploaded_image.getvalue())
        temp_path = tmp_file.name
    with Image.open(temp_path) as img:
        st.image(img, caption="Uploaded Receipt", use_column_width=True)

        extracted = extract_expenses(img)

        if extracted:
            st.subheader("📋 Extracted Information")
            with st.expander("🔍 View Raw Extracted JSON"):
                st.json(extracted)

            total = extracted.get("total_amount", 0.0)
            date = extracted.get("transaction_date", "N/A")
            store = extracted.get("store_name", "N/A")
            item_list = extracted.get("items", [])

            st.write(f"🛍️ Store: **{store}**")
            st.write(f"🗓️ Date: **{date}**")
            st.write(f"💰 Total: **₹{total:.2f}**")

            categorized_items = []
            for item in item_list:
                name = item.get("name", "Unnamed")
                price = item.get("price", 0.0)
                quantity = item.get("quantity", 1)
                category = tag_expense(name)
                icon = CATEGORY_ICONS.get(category, "📦")

                categorized_items.append({
                    "name": name,
                    "price": price,
                    "quantity": quantity,
                    "category": category,
                    "icon": icon
                })

            # --- Display as Table ---
            st.markdown("### 🧾 Item Breakdown by Category")
            for entry in categorized_items:
                st.markdown(f"{entry['icon']} **{entry['name']}** - ₹{entry['price']} × {entry['quantity']} → Category: _{entry['category']}_")

            # --- Chat Log for Debugging (Optional) ---
            st.session_state.chat_logs.append({
                "store": store,
                "date": date,
                "total": total,
                "items": categorized_items
            })
