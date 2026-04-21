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
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Use latest model
model = genai.GenerativeModel("models/gemini-flash-latest")

# -------------------- STYLING --------------------
st.markdown("""
<style>
.main {
    background: linear-gradient(to right, #eef2f3, #ffffff);
}
.stButton>button {
    border-radius: 10px;
    background-color: #4CAF50;
    color: white;
    font-weight: bold;
}
.card {
    padding: 20px;
    border-radius: 15px;
    background-color: #ffffff;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.title("🗳️ Election Process Education Assistant")
st.markdown("### Learn elections in a simple, interactive, and engaging way 🚀")

# -------------------- SIDEBAR --------------------
option = st.sidebar.radio(
    "📚 Explore",
    ["🏠 Overview", "📋 Step-by-Step", "📅 Timeline", "💬 Ask AI"]
)

# -------------------- HELPER FUNCTION --------------------
def get_response(prompt):
    response = model.generate_content(prompt)
    return response.text

# -------------------- OVERVIEW --------------------
if option == "🏠 Overview":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📘 What is an Election?")

    if st.button("Explain in Simple Terms"):
        with st.spinner("Thinking..."):
            prompt = "Explain the election process in very simple terms with bullet points."
            st.markdown(get_response(prompt))

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------- STEP BY STEP --------------------
elif option == "📋 Step-by-Step":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🪜 Step-by-Step Election Process")

    if st.button("Show Full Process"):
        with st.spinner("Generating steps..."):
            prompt = """
            Explain step-by-step how elections are conducted in India.
            Format:
            - Step number
            - Title
            - 1-2 line explanation
            """
            st.markdown(get_response(prompt))

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------- TIMELINE --------------------
elif option == "📅 Timeline":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📆 Election Timeline")

    if st.button("Show Timeline"):
        with st.spinner("Creating timeline..."):
            prompt = """
            Explain election timeline in India in chronological order.
            Include stages from announcement to result.
            Keep it short and structured.
            """
            st.markdown(get_response(prompt))

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------- CHAT --------------------
elif option == "💬 Ask AI":
    st.subheader("🤖 Chat with Election Assistant")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    user_input = st.text_input("Ask anything about elections...")

    col1, col2 = st.columns([1,1])

    with col1:
        if st.button("Ask"):
            if user_input:
                with st.spinner("Thinking..."):
                    prompt = f"""
                    Answer clearly and simply about elections:
                    {user_input}
                    """
                    response = get_response(prompt)

                    st.session_state.chat.append(("You", user_input))
                    st.session_state.chat.append(("AI", response))

    with col2:
        if st.button("Clear Chat"):
            st.session_state.chat = []

    # Display chat
    for sender, msg in st.session_state.chat:
        if sender == "You":
            st.markdown(f"**🧑 You:** {msg}")
        else:
            st.markdown(f"**🤖 AI:** {msg}")

# -------------------- FOOTER --------------------
st.markdown("---")
st.markdown("Built with ❤️ using Google Gemini + Streamlit | #BuildWithAI")