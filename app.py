import streamlit as st
from groq import Groq

# ✅ Streamlit secrets only
if "GROQ_API_KEY" not in st.secrets:
    st.error("❌ GROQ_API_KEY not found")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("📚 AI Study Planner Agent")

# Inputs
goal = st.text_input("Enter your goal")
days = st.number_input("Days", min_value=1, value=30)
hours = st.number_input("Hours/day", min_value=1, value=2)

# 🆕 Extra custom input
extra = st.text_area("Any specific requirements? (optional)",
                     placeholder="Example: Focus more on projects, skip theory, include revision...")

# Session storage
if "plan" not in st.session_state:
    st.session_state.plan = ""

def generate_plan(goal, days, hours, extra):
    prompt = f"""
    Create a {days}-day study plan for: {goal}
    Daily time: {hours} hours

    Additional instructions:
    {extra if extra else "No special requirements"}

    Include:
    - Day-wise tasks
    - Practical tasks
    - Weekly revision
    - Keep it simple and clear and very basic study plan that i can become very confident
    """

    try:
        res = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}]
        )
        return res.choices[0].message.content

    except Exception as e:
        return f"❌ Error: {str(e)}"

# Generate Plan
if st.button("Generate Plan"):
    if goal:
        with st.spinner("Generating..."):
            st.session_state.plan = generate_plan(goal, days, hours, extra)

# Show Plan
if st.session_state.plan:
    st.subheader("📅 Study Plan")
    st.write(st.session_state.plan)

    if st.button("❌ I Missed Today"):
        adjust_prompt = f"""
        Adjust this study plan since user missed 1 day:

        {st.session_state.plan}

        Keep user preferences in mind:
        {extra if extra else "No special requirements"}

        Redistribute tasks smartly.
        """

        try:
            res = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": adjust_prompt}]
            )
            st.session_state.plan = res.choices[0].message.content
            st.success("Plan Adjusted!")

        except Exception as e:
            st.error(e)