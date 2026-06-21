from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from core.pdf_parser import extract_text_from_pdf
from core.chunking import chunking_with_overlapping
from core.pinecone_store import upsert, embedding_model
from core.retrieval import retrieve
from core.generation import generate_response
last_5_conversation = []
def add_context(query,response):
    
    last_5_conversation.append({
        "user's query":query,
        "customer support assistant's response":response
    })
    return last_5_conversation[-10:]
app = FastAPI()

class ChatRequest(BaseModel):
    query: str
    session_id: str 

@app.post("/admin/upload")

@app.post("/chat")
def chat(request: ChatRequest):
    context = retrieve(request.query)
    response = generate_response( query=f"Customer query: {request.query}\n\nRelevant context:\n{context}",conversation_history= last_5_conversation)
    last_5_conversation = add_context(query=request.query,response=response)
    pass

@app.get("/", response_class=HTMLResponse)
def customer_ui():
    return "<h1>Zeno customer chat — placeholder</h1>"


@app.get("/admin", response_class=HTMLResponse)
async def admin_ui():
    return "<h1>Zeno admin upload — placeholder</h1>"