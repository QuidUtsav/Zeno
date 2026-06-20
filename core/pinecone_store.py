#pinecone_store
from pinecone import Pinecone
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
load_dotenv()

pc = Pinecone(api_key=os.getenv("pc_api_key"))
index = pc.Index("zeno")
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def upsert(chunks,embeddings,filename):
    vectors=[]
    for chunk,embedding in zip(chunks,embeddings):
        vectors.append({
            "id":f'{filename}_{chunk["id"]}',
            "values":embedding.tolist(),
            "metadata":{
                "text":chunk["text"],
                "source":filename
            }
        })
    index.upsert(vectors=vectors)
    
    