
import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

# ==========================================
# 1. LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = "gemini-3.8-flash"


# ==========================================
# 2. STREAMLIT PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="NOVA AI",
    page_icon="N",
    layout="centered"
)


# ==========================================
# 3. CUSTOM CSS DESIGN
# ==========================================

st.markdown("""
<style>

.stApp {
    background-color: #0E1117;
    color: white;
}

.block-container {
    max-width: 850px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1 {
    color: #A78BFA;
    text-align: center;
}

.subtitle {
    text-align: center;
    color: #9CA3AF;
    font-size: 17px;
    margin-bottom: 25px;
}

[data-testid="stChatMessage"] {
    border-radius: 12px;
    padding: 12px;
}

[data-testid="stChatInput"] {
    border-radius: 15px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 4. GEMINI CLIENT CONNECTION
# ==========================================

@st.cache_resource
def get_client():

    return genai.Client(
        api_key=API_KEY,
        http_options=types.HttpOptions(
            timeout=120000
        )
    )


# ==========================================
# 5. SESSION STATE INITIALIZATION
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat" not in st.session_state:
    st.session_state.chat = None


# ==========================================
# 6. CREATE GEMINI CHAT SESSION
# ==========================================

def create_new_chat():

    client = get_client()

    return client.chats.create(
        model=MODEL_NAME
    )


if not API_KEY:

    st.error(
        "Gemini API key not found. "
        "Please check your .env file."
    )

    st.stop()


if st.session_state.chat is None:

    try:
        st.session_state.chat = create_new_chat()

    except Exception as error:

        st.error(f"Gemini connection failed: {error}")
        st.stop()


# ==========================================
# 7. SIDEBAR
# ==========================================

with st.sidebar:

    st.title("NOVA AI")

    st.caption("Your personal AI assistant")

    st.divider()

    if st.button(
        "＋ New Chat",
        use_container_width=True
    ):

        st.session_state.messages = []
        st.session_state.chat = None

        st.rerun()

    st.divider()

    st.write("Powered by Google Gemini")

    st.caption("NOVA AI | Version 1.0")


# ==========================================
# 8. MAIN CHAT INTERFACE
# ==========================================

st.title("NOVA AI")

st.markdown(
    '<p class="subtitle">'
    'Your intelligent AI assistant'
    '</p>',
    unsafe_allow_html=True
)

st.divider()


# ==========================================
# 9. WELCOME MESSAGE
# ==========================================

if not st.session_state.messages:

    st.markdown("### Welcome to NOVA AI!")

    st.write(
        "Ask me anything. "
        "Let's build something intelligent."
    )


# ==========================================
# 10. DISPLAY CHAT HISTORY
# ==========================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ==========================================
# 11. CHAT INPUT
# ==========================================

prompt = st.chat_input("Message NOVA AI...")


# ==========================================
# 12. SEND MESSAGE AND STREAM RESPONSE
# ==========================================

if prompt:

    # Display user message
    with st.chat_message("user"):

        st.markdown(prompt)

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Generate assistant response
    with st.chat_message("assistant"):

        try:

            def response_generator():

                response_stream = (
                    st.session_state.chat.send_message_stream(
                        prompt
                    )
                )

                for chunk in response_stream:

                    if chunk.text:

                        yield chunk.text

            answer = st.write_stream(
                response_generator()
            )

            # Save assistant response
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as error:

            st.error(
                f"Gemini request failed: "
                f"{type(error).__name__}: {error}"
            )

            st.info(
                "Please try again when the Gemini API "
                "is available."
            )


# ==========================================
# 13. FOOTER
# ==========================================

st.markdown("---")

st.caption(
    "NOVA AI | Built with Python, Streamlit and Gemini"
)
