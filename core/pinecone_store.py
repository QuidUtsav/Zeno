#storing the given doc we get in pinecoe
from pinecone import Pinecone
import os
from dotenv import load_dotenv
load_dotenv()


pinecone = Pinecone(api_key=os.getenv("pc_api_key"))
index = pinecone.Index("zeno")

def upsert(chunks, embeddings):
    
    index.upsert(vectors=[{
        "id":chunks["id"],
        "values":embeddings,
        "metadata":{"text":chunks["text"]}
    }])
    
