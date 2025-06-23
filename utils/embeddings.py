from typing import List, Dict
from services import rag

def get_embeddings_from_chunks(chunks: List[Dict]) -> List[Dict]:
    texts = [chunk["content"] for chunk in chunks if chunk.get("content")]
    embeddings = rag.embed_texts(texts)

    embedded_chunks = []
    for chunk, embedding in zip(chunks, embeddings):
        chunk["embedding"] = embedding
        embedded_chunks.append(chunk)

    return embedded_chunks
