import os
import streamlit as st
import google.generativeai as genai

# App Page Configuration
st.set_page_config(
    page_title="Abdallah AI",
    page_icon="🤖",
    layout="centered"
)

# App Header
st.title("🤖 Abdallah AI")
st.markdown("Your intelligent, reliable, and sharp personal AI assistant.")

# Configure the AI API
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.warning("⚠️ Please set your Gemini API key in the Streamlit Secrets or environment variables to start chatting.")
else:
    genai.configure(api_key=api_key)

    # Initialize the Gemini Model with a System Instruction defining its identity
    system_instruction = (
        "You are Abdallah AI, an intelligent, reliable, professional, "
        "and sharp personal AI assistant. Always introduce yourself as Abdallah AI "
        "if asked, and maintain a helpful, smart, and engaging tone."
    )
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_instruction
    )

    # Initialize chat session history in Streamlit session state
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    # Display chat history on app rerun
    for message in st.session_state.chat_session.history:
        role = "user" if message.role == "user" else "assistant"
        with st.chat_message(role):
            st.markdown(message.parts[0].text)

    # Accept user input from the chat box at the bottom
    if user_prompt := st.chat_input("Ask Abdallah AI anything..."):
        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):
            with st.spinner("Abdallah AI is thinking..."):
                try:
                    response = st.session_state.chat_session.send_message(user_prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
