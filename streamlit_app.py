import streamlit as st
import requests
import json

# Update the API_URL to use the service name from docker-compose
API_URL = "http://backend:8000"

# Page configuration
st.set_page_config(
    page_title="Field Service Agent",
    page_icon="🤖",
    layout="wide"
)

# Sidebar for document upload
with st.sidebar:
    st.title("📚 Knowledge Hub")
    uploaded_files = st.file_uploader("Choose PDF files", type=['pdf'], accept_multiple_files=True)
    
    if uploaded_files:
        if st.button("Process Documents", key="process_docs"):
            files = [("files", file) for file in uploaded_files]
            
            try:
                response = requests.post(f"{API_URL}/upload", files=files)
                
                if response.status_code == 200:
                    st.success(response.json()["message"])
                else:
                    st.error(f"Error processing files: {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("Failed to connect to the backend server.")

# Main content
st.title("🤖 Field Service Agent")

# Query section with structured input
st.header("Ask Your Question")

# Add question type selector
question_type = st.selectbox(
    "What type of information are you looking for?",
    [
        "Technical Specifications",
        "Maintenance Procedures",
        "Troubleshooting Steps",
        "Safety Guidelines",
        "Operating Instructions",
        "Other (Please specify)"
    ]
)

# Main question input
query = st.text_input(
    "Enter your specific question:",
    placeholder="e.g., What are the maintenance steps for..."
)

if query:
    # Format the query based on question type
    formatted_query = f"Question Type: {question_type}\nSpecific Question: {query}\n\nPlease provide information ONLY from the uploaded documents."
    
    if st.button("Submit Question"):
        try:
            response = requests.post(
                f"{API_URL}/query",
                json={"query": formatted_query}
            )
            
            if response.status_code == 200:
                answer = response.json()["answer"]
                st.write("Answer:", answer)
            else:
                error_msg = response.json().get("error", "Unknown error occurred")
                st.error(f"Error: {error_msg}")
        except requests.exceptions.ConnectionError:
            st.error("Failed to connect to the backend server.")

# Display current context
if uploaded_files:
    with st.sidebar:
        st.markdown("---")
        st.markdown("**📁 Current Knowledge Base:**")
        for file in uploaded_files:
            st.markdown(f"- {file.name}")

# Add some usage instructions
with st.sidebar:
    st.header("How to use")
    st.markdown("""
    1. Upload one or more PDF files using the file uploader
    2. Click 'Process Documents' to analyze the files
    3. Enter your question in the text input
    4. Click 'Submit Question' to get answers about your documents
 
    """)
