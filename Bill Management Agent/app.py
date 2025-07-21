import os
import streamlit as st
from dotenv import load_dotenv
from PIL import Image
import tempfile
import json
import google.generativeai as genai
from autogen.agentchat import UserProxyAgent, AssistantAgent, GroupChat, GroupChatManager

# Load API Key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash")

# --- UI CONFIG ---
st.set_page_config(
    page_title="🧾 AI Bill Management Agent", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin: 0;
    }
    
    .upload-section {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(240, 147, 251, 0.2);
    }
    
    .upload-section h3 {
        color: white;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .category-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        transition: transform 0.2s ease;
    }
    
    .category-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    
    .category-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .expense-item {
        background: #f8fafc;
        padding: 0.8rem 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        border-left: 3px solid #38b2ac;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .expense-name {
        font-weight: 500;
        color: #2d3748;
    }
    
    .expense-cost {
        font-weight: 600;
        color: #38b2ac;
        font-size: 1.1rem;
    }
    
    .summary-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    .summary-section h2 {
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .chat-section {
        background: #f8fafc;
        padding: 2rem;
        border-radius: 15px;
        margin-top: 2rem;
    }
    
    .chat-message {
        margin: 1rem 0;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 2rem;
    }
    
    .agent-message {
        background: white;
        color: #2d3748;
        margin-right: 2rem;
        border-left: 4px solid #38b2ac;
    }
    
    .message-sender {
        font-weight: 600;
        font-size: 0.9rem;
        opacity: 0.8;
        margin-bottom: 0.5rem;
    }
    
    .message-content {
        font-size: 1rem;
        line-height: 1.5;
    }
    
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-top: 4px solid #38b2ac;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #718096;
        font-weight: 500;
        margin-top: 0.5rem;
    }
    
    .processing-spinner {
        text-align: center;
        padding: 2rem;
    }
    
    .success-message {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    .error-message {
        background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("""
    <div class="main-header">
        <h1>💼 AI Bill Management Agent</h1>
        <p>Upload a bill and let AI categorize and analyze your expenses with intelligent insights</p>
    </div>
""", unsafe_allow_html=True)

# Create columns for better layout
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
        <div class="upload-section">
            <h3>📤 Upload Your Bill</h3>
        </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "", 
        type=["jpg", "jpeg", "png"],
        help="Supported formats: JPG, JPEG, PNG"
    )

# Initialize chat log
if 'chat_log' not in st.session_state:
    st.session_state.chat_log = []

# Category icons mapping
CATEGORY_ICONS = {
    "Groceries": "🛒",
    "Dining": "🍽️", 
    "Utilities": "⚡",
    "Shopping": "🛍️",
    "Entertainment": "🎬",
    "Others": "📦",
    "Transportation": "🚗",
    "Healthcare": "🏥",
    "Education": "📚"
}

# --- Helper Functions (same logic, better structure) ---
def process_bill_with_gemini(image_file):
    """Extract expenses from bill image using Gemini Vision"""
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(image_file.read())
            tmp_path = tmp.name

        image = Image.open(tmp_path)

        response = model.generate_content([
            """Extract all expenses from this bill image. Group them into categories: 
            Groceries, Dining, Utilities, Shopping, Entertainment, Transportation, Healthcare, Education, Others. 
            Return as JSON format like {"category": [{"item": "item_name", "cost": "amount"}]}.
            Make sure the cost is just the number without currency symbol.""",
            image
        ])

        text = response.text.strip()
        json_start = text.find("{")
        json_end = text.rfind("}") + 1
        
        if json_start != -1 and json_end != -1:
            data = json.loads(text[json_start:json_end])
            return data, response.text
        else:
            return None, response.text
            
    except Exception as e:
        st.error(f"Error processing bill: {str(e)}")
        return None, str(e)
    finally:
        # Clean up temp file
        if 'tmp_path' in locals():
            os.unlink(tmp_path)

def summarize_expenses_with_gemini(expenses):
    """Generate expense summary using Gemini"""
    try:
        prompt = f"""
        Analyze the following categorized expenses: {expenses}
        
        Provide a comprehensive summary including:
        1. Total expenditure across all categories
        2. Individual category totals
        3. Highest spending category and potential reasons
        4. Any unusual or noteworthy spending patterns
        5. Brief financial insights or recommendations
        
        Format the response in a clear, readable manner.
        """
        
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating summary: {str(e)}"

def calculate_expense_stats(categorized_data):
    """Calculate statistics from categorized expenses"""
    total_amount = 0
    category_totals = {}
    item_count = 0
    
    for category, items in categorized_data.items():
        category_total = 0
        for item in items:
            try:
                cost = float(str(item['cost']).replace('₹', '').replace(',', ''))
                category_total += cost
                item_count += 1
            except (ValueError, KeyError):
                continue
        
        if category_total > 0:
            category_totals[category] = category_total
            total_amount += category_total
    
    return {
        'total_amount': total_amount,
        'category_totals': category_totals,
        'item_count': item_count,
        'category_count': len([c for c in category_totals if category_totals[c] > 0])
    }

# --- AutoGen Agents Setup (same logic) ---
user_proxy = UserProxyAgent(
    name="UserProxy",
    human_input_mode="NEVER",
    code_execution_config={"use_docker": False},
    llm_config=False
)

bill_processing_agent = AssistantAgent(
    name="BillProcessingAgent",
    llm_config=False,
    system_message="You categorize expenses from a bill into standard categories and ensure proper data structure."
)

summary_agent = AssistantAgent(
    name="ExpenseSummarizationAgent", 
    llm_config=False,
    system_message="You analyze categorized expenses, provide insights, and summarize spending trends with actionable recommendations."
)

group_chat = GroupChat(agents=[user_proxy, bill_processing_agent, summary_agent])
manager = GroupChatManager(groupchat=group_chat)

# --- Main Processing Logic ---
if uploaded_file:
    # Success message
    st.markdown('<div class="success-message">✅ File uploaded successfully! Processing your bill...</div>', 
                unsafe_allow_html=True)
    
    # Display uploaded image
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(uploaded_file, caption="Uploaded Bill", use_column_width=True)
    
    # Processing with spinner
    with st.spinner("🔍 Extracting and categorizing expenses..."):
        categorized_data, raw_response = process_bill_with_gemini(uploaded_file)

    if not categorized_data:
        st.markdown('<div class="error-message">❌ Failed to extract expenses from the bill.</div>', 
                   unsafe_allow_html=True)
        with st.expander("View Raw Response"):
            st.text(raw_response)
    else:
        # Calculate statistics
        stats = calculate_expense_stats(categorized_data)
        
        # Agent communication (same logic)
        st.session_state.chat_log = []
        
        # 1. User → Group Manager
        user_proxy.send("Bill uploaded and processed", manager)
        st.session_state.chat_log.append(("UserProxy → GroupManager", "Bill uploaded and processed"))

        # 2. User → BillProcessingAgent  
        user_proxy.send(f"Categorized expenses: {categorized_data}", bill_processing_agent)
        st.session_state.chat_log.append(("UserProxy → BillProcessingAgent", json.dumps(categorized_data, indent=2)))

        # 3. Simulate BillProcessingAgent response
        bp_response = f"✅ Categorization complete! Successfully processed {stats['item_count']} items across {stats['category_count']} categories."
        st.session_state.chat_log.append(("BillProcessingAgent", bp_response))

        # 4. User → ExpenseSummarizationAgent
        user_proxy.send("Generate comprehensive expense analysis", summary_agent)
        st.session_state.chat_log.append(("UserProxy → ExpenseSummarizationAgent", "Generate comprehensive expense analysis"))

        # 5. Generate summary
        with st.spinner("📊 Generating intelligent spending analysis..."):
            summary = summarize_expenses_with_gemini(categorized_data)

        st.session_state.chat_log.append(("ExpenseSummarizationAgent", summary))

        # --- Display Statistics ---
        st.markdown(f"""
            <div class="stats-container">
                <div class="stat-card">
                    <div class="stat-number">₹{stats['total_amount']:,.2f}</div>
                    <div class="stat-label">Total Amount</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{stats['item_count']}</div>
                    <div class="stat-label">Total Items</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{stats['category_count']}</div>
                    <div class="stat-label">Categories</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">₹{stats['total_amount']/stats['item_count']:,.2f}</div>
                    <div class="stat-label">Avg per Item</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # --- Display Categorized Expenses ---
        st.markdown("## 📂 Categorized Expenses")
        
        # Filter out empty categories
        non_empty_categories = {k: v for k, v in categorized_data.items() if v}
        
        for category, items in non_empty_categories.items():
            category_total = sum(float(str(item['cost']).replace('₹', '').replace(',', '')) 
                               for item in items if 'cost' in item)
            icon = CATEGORY_ICONS.get(category, "📦")
            
            st.markdown(f"""
                <div class="category-card">
                    <div class="category-title">
                        {icon} {category} 
                        <span style="margin-left: auto; color: #38b2ac;">₹{category_total:,.2f}</span>
                    </div>
            """, unsafe_allow_html=True)
            
            for item in items:
                if 'item' in item and 'cost' in item:
                    cost = str(item['cost']).replace('₹', '')
                    st.markdown(f"""
                        <div class="expense-item">
                            <span class="expense-name">{item['item']}</span>
                            <span class="expense-cost">₹{cost}</span>
                        </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)

        # --- Display Summary ---
        st.markdown(f"""
            <div class="summary-section">
                <h2>📋 AI Spending Analysis</h2>
                <div style="font-size: 1.1rem; line-height: 1.6;">
                    {summary}
                </div>
            </div>
        """, unsafe_allow_html=True)

        # --- Display Agent Chat Logs ---
        st.markdown("""
            <div class="chat-section">
                <h2>💬 Agent Communication Logs</h2>
        """, unsafe_allow_html=True)
        
        for sender, message in st.session_state.chat_log:
            is_user = "UserProxy" in sender
            message_class = "user-message" if is_user else "agent-message"
            
            st.markdown(f"""
                <div class="chat-message {message_class}">
                    <div class="message-sender">{sender}</div>
                    <div class="message-content">{message}</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # Welcome message when no file is uploaded
    st.markdown("""
        <div style="text-align: center; padding: 3rem; color: #718096;">
            <h3>👆 Upload a bill image to get started</h3>
            <p>Our AI will automatically categorize your expenses and provide intelligent insights</p>
        </div>
    """, unsafe_allow_html=True)