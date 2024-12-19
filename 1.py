import streamlit as st
import PyPDF2
import google.generativeai as genai

# Configure Gemini API Key
genai.configure(api_key="AIzaSyCDbSjkmQrtHRMpa6Cz-8D1-iXUucEwHVw")

def extract_text_from_pdf(pdf_file):
    """Extract and format text from a PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        # Clean up line breaks and merge into paragraphs
        cleaned_text = " ".join([line.strip() for line in text.splitlines() if line.strip()])
        return cleaned_text
    except Exception as e:
        return f"Error reading PDF: {e}"

def ask_gemini_api(question, context=None):
    """Send a question to Gemini API and get a response"""
    try:
        if context:
            prompt = f"Context: {context}\nQuestion: {question}"
        else:
            prompt = f"Question: {question}"
        
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error communicating with Gemini API: {e}"

def load_css(file_path):
    """Load custom CSS from a file"""
    with open(file_path, "r", encoding="utf-8") as f:
        return f"<style>{f.read()}</style>"

# Apply custom CSS
st.markdown(load_css("styles.css"), unsafe_allow_html=True)

# Streamlit main application
title = "Interactive Chatbot"
st.title(title)
st.sidebar.title("Upload Your PDF Files")

# Multiple file upload functionality
uploaded_files = st.sidebar.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

file_texts = {}
if uploaded_files:
    st.write(f"Uploaded {len(uploaded_files)} files!")

    # Extract text from each uploaded file
    file_texts = {uploaded_file.name: extract_text_from_pdf(uploaded_file) for uploaded_file in uploaded_files}

# Ask mode selection
mode = st.radio("Choose the Q&A mode:", options=["PDF Analysis", "Open-ended Q&A"])

if mode == "PDF Analysis":
    if file_texts:
        # Select a file to ask questions about
        selected_file = st.selectbox("Select a file to interact with:", options=file_texts.keys())

        if selected_file:
            # Display the extracted text for the selected file
            st.text_area(f"Extracted Text from {selected_file}", file_texts[selected_file], height=110)

            # Input for user questions
            user_question = st.text_input("Ask a question about the selected document:")

            if user_question:
                with st.spinner("Getting your answer..."):
                    # Use the selected file's text as context
                    context = file_texts[selected_file]
                    answer = ask_gemini_api(user_question, context)
                    st.write("Answer:", answer)
    else:
        st.warning("No files uploaded. Please upload a PDF to use this mode.")

elif mode == "Open-ended Q&A":
    user_question = st.text_input("Ask any question:")

    if user_question:
        with st.spinner("Getting your answer..."):
            # Open-ended question without context
            answer = ask_gemini_api(user_question)
            st.write("Answer:", answer)

# Display instructions for running the app
st.sidebar.info("Run the app locally using: streamlit run app.py")