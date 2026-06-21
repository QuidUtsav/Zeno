from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from core.pdf_parser import extract_text_from_pdf
from core.chunking import chunking_with_overlapping
from core.pinecone_store import upsert, embedding_model
from core.retrieval import retrieve
from core.generation import generate_response

app = FastAPI()


session_histories = {}


def get_history(session_id):
    return session_histories.get(session_id, [])


def update_history(session_id, query, response):
    history = session_histories.get(session_id, [])
    history.append({"role": "user", "content": query})
    history.append({"role": "assistant", "content": response})
    session_histories[session_id] = history[-10:]  # last 5 turns (10 messages)


class ChatRequest(BaseModel):
    query: str
    session_id: str



@app.post("/admin/upload")
def admin_upload(file: UploadFile = File(...)):
    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(file.file)
    elif file.filename.endswith(".txt"):
        text = file.file.read().decode("utf-8")
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type. Upload a .pdf or .txt file.")

    chunks = chunking_with_overlapping(text)
    chunk_texts = [chunk["text"] for chunk in chunks]
    embeddings = embedding_model.encode(chunk_texts)
    upsert(chunks, embeddings, file.filename)

    return {"status": "uploaded", "filename": file.filename, "chunks": len(chunks)}

@app.post("/chat")
def chat(request: ChatRequest):
    context = retrieve(request.query)
    history = get_history(request.session_id)

    response = generate_response(
        query=f"Customer question: {request.query}\n\nRelevant context:\n{context}",
        conversation_history=history
    )

    update_history(request.session_id, request.query, response)

    return {"answer": response, "session_id": request.session_id}


@app.get("/", response_class=HTMLResponse)
def customer_ui():
    return "<h1>Zeno customer chat — placeholder</h1>"


@app.get("/admin", response_class=HTMLResponse)
def admin_ui():
    return "<h1>Zeno admin upload — placeholder</h1>"