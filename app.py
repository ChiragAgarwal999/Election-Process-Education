import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# -------------------- CONFIG --------------------
st.set_page_config(
    page_title="Election Assistant",
    page_icon="🗳️",
    layout="wide"
)

# Load env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("❌ GOOGLE_API_KEY not found")
    st.stop()

genai.configure(api_key=api_key)

# KEEPING YOUR MODEL EXACTLY SAME ✅
model = genai.GenerativeModel("models/gemini-flash-latest")

# -------------------- STYLING --------------------
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #f5f5dc, #d4edda);
}
.stButton>button {
    border-radius: 12px;
    background: linear-gradient(135deg, #2e7d32, #66bb6a);
    color: white;
    font-weight: bold;
}
.card {
    padding: 20px;
    border-radius: 18px;
    background: #ffffff;
    box-shadow: 0 6px 15px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}
.user-msg {
    background: #c8e6c9;
    padding: 10px;
    border-radius: 10px;
    margin: 5px 0;
}
.ai-msg {
    background: #fff3e0;
    padding: 10px;
    border-radius: 10px;
    margin: 5px 0;
}
</style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.title("🗳️ Election Process Education Assistant")
st.markdown("### Helping first-time voters understand elections easily 🚀")

# -------------------- LANGUAGE --------------------
language = st.sidebar.selectbox("🌐 Language", ["English", "Hindi"])

def add_language(prompt):
    if language == "Hindi":
        return prompt + " Answer in Hindi."
    return prompt

# -------------------- SIDEBAR --------------------
option = st.sidebar.radio(
    "📚 Explore",
    ["🏠 Overview", "📋 Step-by-Step", "📅 Timeline", "🧠 Quiz", "💬 Ask AI"]
)

# -------------------- HELPER FUNCTION --------------------
def get_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# -------------------- OVERVIEW --------------------
if option == "🏠 Overview":
    st.markdown('<div class="card">', unsafe_allow_html=True)

    if st.button("Explain Election"):
        with st.spinner("Thinking..."):
            prompt = add_language("""
            Explain election process:
            - very simple
            - bullet points
            - beginner friendly
            """)
            st.success("✅ Generated!")
            st.markdown(get_response(prompt))

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------- STEP BY STEP --------------------
elif option == "📋 Step-by-Step":
    st.markdown('<div class="card">', unsafe_allow_html=True)

    if st.button("Show Steps"):
        with st.spinner("Generating..."):
            prompt = add_language("""
            Explain election process in India:
            Step 1, Step 2...
            short explanation each
            """)
            st.success("✅ Steps Ready!")
            st.markdown(get_response(prompt))

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------- TIMELINE --------------------
elif option == "📅 Timeline":
    st.markdown('<div class="card">', unsafe_allow_html=True)

    if st.button("Show Timeline"):
        with st.spinner("Creating..."):
            prompt = add_language("""
            Give election timeline in India:
            announcement → nomination → voting → counting → result
            short format
            """)
            st.success("✅ Timeline Generated!")
            st.markdown(get_response(prompt))

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------- QUIZ --------------------
elif option == "🧠 Quiz":
    st.subheader("🧠 Test Your Knowledge")

    score = 0

    q1 = st.radio(
        "Who conducts elections in India?",
        ["Supreme Court", "Election Commission", "Prime Minister"]
    )

    q2 = st.radio(
        "Minimum voting age in India?",
        ["16", "18", "21"]
    )

    if st.button("Submit Quiz"):
        if q1 == "Election Commission":
            score += 1
        if q2 == "18":
            score += 1

        st.success(f"Your Score: {score}/2")

# -------------------- CHAT --------------------
elif option == "💬 Ask AI":
    st.subheader("🤖 Ask Anything")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    user_input = st.text_input("Type your question...")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Ask"):
            if user_input:
                with st.spinner("Thinking..."):
                    prompt = add_language(f"Explain simply: {user_input}")
                    response = get_response(prompt)

                    st.session_state.chat.append(("You", user_input))
                    st.session_state.chat.append(("AI", response))

    with col2:
        if st.button("Clear Chat"):
            st.session_state.chat = []

    for sender, msg in st.session_state.chat:
        if sender == "You":
            st.markdown(f'<div class="user-msg">🧑 {msg}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ai-msg">🤖 {msg}</div>', unsafe_allow_html=True)

# -------------------- FOOTER --------------------
st.markdown("---")
st.markdown("🌿 Built with Google Gemini + Streamlit | #BuildWithAI #PromptWarsVirtual")