import streamlit as st
import google.generativeai as genai
import tempfile
import docx
import fitz  # PyMuPDF for PDFs

# ===============================
# CONFIGURE GEMINI API
# ===============================
API_KEY = "YOUR_GEMINI_API_KEY"  # 🔥 Replace this with st.secrets or your real key
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# ===============================
# HELPER FUNCTIONS
# ===============================
def extract_text_from_file(uploaded_file):
    """Extract text from PDF, DOCX, or TXT files."""
    file_type = uploaded_file.name.split('.')[-1].lower()
    text = ""

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    if file_type == "pdf":
        doc = fitz.open(tmp_path)
        for page in doc:
            text += page.get_text()
    elif file_type == "docx":
        doc = docx.Document(tmp_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    elif file_type == "txt":
        with open(tmp_path, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        text = "Unsupported file type."

    return text


def chat_with_ai(prompt, context=""):
    """Send user prompt + context to Gemini."""
    try:
        full_prompt = f"{context}\n\nUser: {prompt}\nAI:"
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# ===============================
# STREAMLIT UI
# ===============================
st.set_page_config(page_title="Gemini AI Chatbot", page_icon="🤖", layout="wide")

st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🤖 Gemini AI Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Ask me anything, or upload a document and I’ll help!</p>", unsafe_allow_html=True)

# Sidebar
st.sidebar.header("Settings ⚙️")
api_key_input = st.sidebar.text_input("Enter Gemini API Key:", type="password")
if api_key_input:
    genai.configure(api_key="AIzaSyCvI0c_O4w6RZKAl7LHveEQISL6wzHzVSg")

# Document Upload
uploaded_file = st.file_uploader("📂 Upload a document (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
doc_text = ""
if uploaded_file:
    doc_text = extract_text_from_file(uploaded_file)
    st.success("Document uploaded successfully!")
    with st.expander("📖 Preview Extracted Text"):
        st.write(doc_text[:1000] + "..." if len(doc_text) > 1000 else doc_text)

# Chat Section
st.markdown("---")
user_input = st.text_input("💬 Type your message:", "")

if st.button("🚀 Send"):
    if user_input.strip():
        answer = chat_with_ai(user_input, doc_text)
        st.markdown(f"<div style='padding:10px;background:#DCF8C6;border-radius:10px;'><b>You:</b> {user_input}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='padding:10px;background:#F1F0F0;border-radius:10px;'><b>Gemini:</b> {answer}</div>", unsafe_allow_html=True)
    else:
        st.warning("Please enter a message.")

# Footer
st.markdown("<hr><center>Built with ❤️ using Streamlit & Gemini</center>", unsafe_allow_html=True)
