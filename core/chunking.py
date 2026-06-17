def chunking_with_overlapping(text,chunk_size=200,overlap=50):
    tokens = text.split(" ")
    i=0;
    chunks=[]
    while(i<len(tokens)):
        context_window=tokens[i:i+chunk_size]
        chunks.append({
            "id":len(chunks),
            "text":" ".join(context_window)})
        i+=chunk_size-overlap    

    return chunks