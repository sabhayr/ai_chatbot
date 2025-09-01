import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖", layout="centered")

st.title("🤖 Gemini AI Chatbot")
st.write("Chat with Google's Gemini model!")

# Load API Key from Streamlit secrets
genai.configure(api_key=st.secrets.get("GEMINI_API_KEY", "your_gemini_api_key_here"))

model = genai.GenerativeModel("gemini-pro")

def chat_with_ai(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

user_input = st.text_input("Type your message:", "")

if st.button("Send"):
    if user_input.strip():
        answer = chat_with_ai(user_input)
        st.write(f"**Gemini:** {answer}")
    else:
        st.warning("Please enter a message.")
