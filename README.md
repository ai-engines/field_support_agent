# Field Service Agent - Document Q&A System

An intelligent document Q&A system that processes technical documentation and provides accurate answers using AI. 
The system is designed to work exclusively with uploaded documents, preventing hallucination by limiting responses to available content.

## 🌟 Features

- 📚 PDF Document Processing
- 🤖 AI-Powered Question Answering
- 🎯 Zero Hallucination Design
- 🔍 Context-Aware Responses
- 📱 User-Friendly Interface
- 🚀 Docker Containerization

## 🛠 Tech Stack

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **AI/ML**: 
  - LangChain
  - OpenAI GPT-4
  - FAISS Vector Store
- **Containerization**: Docker

## 🚀 Quick Start

### Prerequisites

1. Docker and Docker Compose installed
2. OpenAI API key
3. Git (for cloning the repository)

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/field-service-agent.git
   cd field-service-agent
   ```

2. Create a `.env` file in the project root:
   ```bash
   OPENAI_API_KEY=<your-openai-api-key>
   ```

3. Build and start the containers:
   ```bash
   docker-compose up --build
   ```

4. Access the application:

- Frontend: http://localhost:8501
- Backend API: http://localhost:8000

## 📖 Usage

1. Open the Streamlit interface at http://localhost:8501
2. Upload PDF documents through the Knowledge Hub sidebar
3. Select the type of information you're looking for
4. Enter your specific question
5. Get AI-powered answers based on your documents

## 🔒 Security Notes

- The system processes documents temporarily and doesn't store them permanently
- All processing is done within isolated Docker containers

## 🛑 Limitations

- Only supports PDF files
- Responses are limited to information found in uploaded documents
- Maximum file size depends on available system resources



