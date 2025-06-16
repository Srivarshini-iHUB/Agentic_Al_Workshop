import streamlit as st
from utils import get_recommendation

st.set_page_config(page_title="Health Policy Recommender", layout="centered")

st.title("🏥 Health Policy Recommendation Agent")
st.subheader("Get personalized health insurance suggestions from HealthSecure Insurance Ltd.")

# Input section
age = st.number_input("Age", min_value=0, max_value=120, step=1)
family_type = st.selectbox("Family Type", ["Individual", "Family", "Senior"])
dependents = st.number_input("Number of Dependents (0 if none)", min_value=0, step=1)

st.markdown("#### Special Requirements")
maternity = st.checkbox("Maternity & Newborn Care")
dental_vision = st.checkbox("Dental & Vision Care")
travel = st.checkbox("International Travel")
mental_health = st.checkbox("Mental Health & Wellness Support")

# Results
if st.button("Suggest Plans"):
    recommendations = get_recommendation(
        age, family_type, dependents,
        maternity, dental_vision, travel, mental_health
    )
    st.success("🎯 Recommended Plan(s):")
    for plan in recommendations:
        st.markdown(plan)
