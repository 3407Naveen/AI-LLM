
import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load API key
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# Page configuration
st.set_page_config(
    page_title="NOVA AI",
    page_icon="🤖",
    layout="centered"
)

# Initialize Gemini client
@st.cache_resource
def get_client():
    return genai.Client(
        api_key=API_KEY,
        http_options=types.HttpOptions(timeout=30000)
    )

# Initialize chat session
if "chat" not in st.session_state:
    st.session_state.chat = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# Create chat
if API_KEY and st.session_state.chat is None:
    client = get_client()
    st.session_state.chat = client.chats.create(
        model="gemini-3.8-flash"
    )

# Header
st.title("🤖 NOVA AI")
st.caption("Your personal AI assistant")

st.divider()

# Sidebar
with st.sidebar:
    st.title("NOVA AI")
    st.write("AI Assistant powered by Gemini")

    if st.button("New Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat = get_client().chats.create(
            model="gemini-3.8-flash"
        )
        st.rerun()

    st.divider()
    st.caption("Built with Python, Streamlit and Gemini API")

# Check API key
if not API_KEY:
    st.error("Gemini API key not found. Check your .env file.")
    st.stop()

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Message NOVA AI...")

if prompt:
    # Display user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        try:
            def generate_response():
                response_stream = (
                    st.session_state.chat.send_message_stream(prompt)
                )

                for chunk in response_stream:
                    if chunk.text:
                        yield chunk.text

            answer = st.write_stream(generate_response())

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as error:
            st.error(
                f"Gemini request failed: {type(error).__name__}: {error}"
            )
