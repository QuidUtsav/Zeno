#retrieving the highest matched relevant chunk from the pinecone

from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def retrieve(query,top_k=5):
    
    #first convert the query with same embedding model i set in pinceconee web
    query_embedding = model.encode(query)
    
    #next use index.query and get result
    
    #slice through result to get text data and use generation.py to reply
    
    
    pass