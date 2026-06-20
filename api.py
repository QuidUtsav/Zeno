from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from core.pdf_parser import extract_text_from_pdf
from core.chunking import chunking_with_overlapping
from core.pinecone_store import upsert, embedding_model
from core.retrieval import retrieve

app = FastAPI()

class ChatRequest(BaseModel):
    query: str
    session_id: str 

@app.post("/admin/upload")

@app.post("/chat")
async def chat(request: ChatRequest):
    context = retrieve(request.query)
    pass

@app.get("/", response_class=HTMLResponse)
async def customer_ui():
    return "<h1>Zeno customer chat — placeholder</h1>"


@app.get("/admin", response_class=HTMLResponse)
async def admin_ui():
    return "<h1>Zeno admin upload — placeholder</h1>"