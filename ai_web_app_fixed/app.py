
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="centered")

st.title("🤖 AI Chatbot")
st.write("Talk to your AI assistant right here!")

client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", "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"))

def chat_with_ai(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

user_input = st.text_input("Type your message:", "")

if st.button("Send"):
    if user_input.strip():
        answer = chat_with_ai(user_input)
        st.write(f"**AI:** {answer}")
    else:
        st.warning("Please enter a message.")
