import streamlit as st
from agents.agent_executor import initialize_agent


st.title("🧳 Travel Assistant AI")

city = st.text_input("Enter your destination city")

if st.button("Ask AI") and city:
    st.info("Fetching information...")
    agent = initialize_agent()
    response = agent.invoke({"input": f"Tell me the current weather and top attractions in {city}.", "chat_history": []})
    st.success(response['output'])
