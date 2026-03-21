import streamlit as st
from google import genai
from datetime import datetime

# -------------------------
# Step 1: Configure API
# -------------------------
client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

MODEL_NAME = "gemini-3-flash-preview"


# -------------------------
# Step 2: AI Query Function
# -------------------------
def query(user_query):
    # ✅ Handle date manually
    if "date" in user_query.lower():
        return datetime.now().strftime("%d %B %Y")

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=user_query
        )

        # safer response handling
        if hasattr(response, "text") and response.text:
            return response.text
        else:
            return "No response generated."

    except Exception as e:
        return f"Error: {str(e)}"


# -------------------------
# Step 3: Session State
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []


# -------------------------
# Step 4: UI Title
# -------------------------
st.title("ChatGPT 2.0 🤖")


# -------------------------
# Step 5: Chat Styling
# -------------------------
st.markdown("""
<style>
.chat-container {
    max-width: 700px;
    margin: auto;
    display: flex;
    flex-direction: column;
}

.chat-row {
    display: flex;
    align-items: flex-end;
    margin: 5px;
}

.chat-row.user {
    justify-content: flex-end;
}

.chat-row.assistant {
    justify-content: flex-start;
}

.avatar {
    font-size: 24px;
    margin: 5px;
}

.message {
    padding: 10px;
    border-radius: 10px;
    max-width: 60%;
    word-wrap: break-word;
}

.user-message {
    background-color: #DCF8C6;
    text-align: right;
}

.assistant-message {
    background-color: #F1F0F0;
    text-align: left;
}
</style>
""", unsafe_allow_html=True)


# -------------------------
# Step 6: Chat Input
# -------------------------
user_input = st.chat_input("Enter your query...")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.spinner("Thinking..."):
        ai_response = query(user_input)

    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_response
    })


# -------------------------
# Step 7: Display Chat
# -------------------------
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f"""
            <div class="chat-row user">
                <div class="message user-message">{msg["content"]}</div>
                <div class="avatar">👤</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div class="chat-row assistant">
                <div class="avatar">🤖</div>
                <div class="message assistant-message">{msg["content"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown('</div>', unsafe_allow_html=True)