import chromadb
from chromadb.config import Settings
from typing import List, Dict
from services.rag import embed_texts
from utils.chroma_client import get_chroma_client

chroma_client = get_chroma_client()

def save_chunks_to_chroma(chunks: List[Dict], collection_name: str):
    collection = chroma_client.get_or_create_collection(name=collection_name)

    ids = [f"chunk_{i}" for i in range(len(chunks))]
    embeddings = [chunk["embedding"] for chunk in chunks]
    documents = [chunk["content"] for chunk in chunks]
    metadatas = [{"page": chunk["page"], "type": chunk["type"]} for chunk in chunks]

    # Debug check
    print(f"Saving {len(chunks)} chunks to collection '{collection_name}'")
    print("Sample embedding shape:", len(embeddings[0]) if embeddings else "None")

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )

    # chroma_client.persist()
    # print("[DEBUG] Chroma DB persisted to disk.")

def query_chroma(query: str, collection_name: str, top_k: int = 5) -> List[Dict]:
    """ 
        Given a user query, embed it and search ChromDB
        Returns top k documents with metadata 
    """
    collection = chroma_client.get_or_create_collection(name=collection_name)

    query_embedding = embed_texts([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents","metadatas","distances"]
    )

    matches=[]
    for doc, meta, dist in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
        matches.append(
            {
                "content":doc,
                "metadata":meta,
                "distance":dist
            }
        )

    return matches