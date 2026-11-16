
import streamlit as st

st.set_page_config(
    page_title="NOVA AI",
    page_icon="🤖"
)

st.title("NOVA AI")
st.subheader("Your AI Assistant")

st.success("Streamlit is working!")

st.write("Welcome to NOVA AI.")
st.write("Your first web application is running successfully.")

name = st.text_input("Enter your name")

if name:
    st.write(f"Hello, {name}! Welcome to NOVA AI.")
