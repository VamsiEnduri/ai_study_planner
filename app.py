import streamlit as st
from groq import Groq

# ✅ Only Streamlit Secrets
if "GROQ_API_KEY" not in st.secrets:
    st.error("❌ GROQ_API_KEY not found in Streamlit Secrets")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("📚 AI Study Planner Agent")

# Inputs
goal = st.text_input("Enter your goal")
days = st.number_input("Days", min_value=1, value=30)
hours = st.number_input("Hours/day", min_value=1, value=2)

# Session storage
if "plan" not in st.session_state:
    st.session_state.plan = ""

def generate_plan(goal, days, hours):
    prompt = f"""
    Create a {days}-day study plan for: {goal}
    Daily time: {hours} hours

    Include:
    - Day-wise tasks
    - Practice tasks
    - Weekly revision
    - Simple language
    """

    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return res.choices[0].message.content

# Generate Plan
if st.button("Generate Plan"):
    if goal:
        with st.spinner("Generating..."):
            st.session_state.plan = generate_plan(goal, days, hours)

# Show Plan
if st.session_state.plan:
    st.subheader("📅 Study Plan")
    st.write(st.session_state.plan)
