#retrieving the highest matched relevant chunk from the pinecone

from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
load_dotenv()

pc = Pinecone(api_key=os.getenv("pc_api_key"))
index = pc.Index("zeno")

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
def retrieve(query,top_k=5):
    
    query_embedding = model.encode(query).tolist()
    
    result = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True   
    )
    
    result = result["matches"][:top_k]
    result_text=[]
    for r in result:
        result_text.append(r["metadata"]["text"])
    return " ".join(result_text)


