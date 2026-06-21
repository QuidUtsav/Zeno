#retrieving the highest matched relevant chunk from the pinecone

from core.pinecone_store import index, embedding_model
def retrieve(query,top_k=5):
    
    query_embedding = embedding_model.encode(query).tolist()
    
    result = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True   
    )
    
    result_text=[]
    for r in result:
        result_text.append(r["metadata"]["text"])
    return " ".join(result_text)


