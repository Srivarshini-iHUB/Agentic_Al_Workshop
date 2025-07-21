import streamlit as st
from utils.search_tool import tavily_web_search
from utils.chat_handler import ask_gemini_with_context

st.set_page_config(page_title="Clothing Market Analyst Chatbot")
st.title("🧠 Competitor Analyst Assistant")
st.write("Ask about local clothing stores, peak hours, or promotional strategies.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Example: What are the busiest clothing stores in Coimbatore?")

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append(("user", user_input))

    with st.spinner("🔍 Searching Tavily..."):
        web_data = tavily_web_search(user_input)

    with st.spinner("🧠 Generating insight with Gemini..."):
        ai_reply = ask_gemini_with_context(user_input, web_data)
        st.chat_message("ai").markdown(ai_reply)
        st.session_state.chat_history.append(("ai", ai_reply))
