
import streamlit as st
import google.generativeai as genai

# Configure Gemini API key
genai.configure(api_key="AIzaSyDjKnYmE12Hczu4wXvrmnJKsQpNyjE907M")

# Use a supported model (gemini-1.5-pro or gemini-1.5-flash)
model = genai.GenerativeModel("gemini-1.5-flash")

# Generate content
response = model.generate_content("Write a short poem about AI and coffee.")
print(response.text)

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
