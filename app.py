from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.prompts import PromptTemplate
import tempfile
import os

app = FastAPI()

# Global variable to store the agent
global_agent = None

class QueryRequest(BaseModel):
    query: str

# Define a custom prompt template
CUSTOM_PROMPT = """You are a Field Service Agent assistant. Your role is to provide accurate information ONLY from the provided documentation. 
If the information is not in the documents, say "I cannot find this information in the provided documents."

Context from documents: {context}

Question: {query}

Please provide a clear and concise answer based ONLY on the information found in the documents. Do not make assumptions or add information from general knowledge.

Answer:"""

@app.post("/upload")
async def upload_files(files: list[UploadFile] = File(...)):
    global global_agent
    
    documents = []
    with tempfile.TemporaryDirectory() as temp_dir:
        for file in files:
            if file.filename.endswith('.pdf'):
                temp_path = os.path.join(temp_dir, file.filename)
                with open(temp_path, 'wb') as f:
                    content = await file.read()
                    f.write(content)
                
                loader = PyPDFLoader(temp_path)
                documents.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)
    vector_store = FAISS.from_documents(docs, OpenAIEmbeddings())
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}  # Limit to top 3 most relevant chunks
    )

    # Create custom tool with the prompt template
    def search_docs(query: str) -> str:
        docs = retriever.get_relevant_documents(query)
        context = "\n".join([doc.page_content for doc in docs])
        prompt = PromptTemplate(
            template=CUSTOM_PROMPT,
            input_variables=["context", "query"]
        )
        
        llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)  # Set temperature to 0 for more focused responses
        response = llm.predict(prompt.format(context=context, query=query))
        return response

    tools = [
        Tool(
            name="Document Search",
            func=search_docs,
            description="Search through the uploaded documents for relevant information"
        )
    ]
    
    llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)
    global_agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        max_iterations=2  # Limit the number of iterations to prevent wandering
    )
    
    return {"message": f"Successfully processed {len(files)} files"}

@app.post("/query")
def query_agent(request: QueryRequest):
    if not global_agent:
        return {"error": "Please upload documents first"}
    
    # Add a reminder to the query
    enhanced_query = f"""Answer this question using ONLY information from the provided documents: {request.query}
    If you cannot find the specific information in the documents, say so clearly."""
    
    response = global_agent.run(enhanced_query)
    return {"answer": response}

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
