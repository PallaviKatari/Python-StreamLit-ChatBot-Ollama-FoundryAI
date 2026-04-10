import streamlit as st
import requests

# ---------------- UI ----------------
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 AI Chatbot (Local - Ollama)")

# ---------------- Ollama API ----------------
def ask_ollama(messages):
    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "llama3",
                "messages": messages,
                "stream": False
            }
        )
        return response.json()["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"

# ---------------- Session State ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- Display Chat ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ---------------- User Input ----------------
user_input = st.chat_input("Type your message...")

if user_input:
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    # Get AI response
    with st.spinner("Thinking... 🤔"):
        response = ask_ollama(st.session_state.messages)

    # Add assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    with st.chat_message("assistant"):
        st.write(response)