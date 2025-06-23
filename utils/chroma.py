import chromadb
from chromadb.config import Settings
from typing import List, Dict
from services.rag import embed_texts
from utils.chroma_client import get_chroma_client

_chroma_client = None

# def get_chroma_client():
#     global _chroma_client
#     if _chroma_client is None:
#         _chroma_client = chromadb.Client(Settings(
#             persist_directory="chroma_store",
#             anonymized_telemetry=False
#         ))
#     return _chroma_client

# chroma_client = chromadb.Client(Settings(
#     persist_directory = "chroma_store",
#     anonymized_telemetry = False
# ))

chroma_client = get_chroma_client()

def save_chunks_to_chroma(chunks: List[Dict], collection_name: str):
    """
    Saves embedded chunks into a chromadb collection.
    Each chunk must have id, embedding, content and metadata
    """

    collection = chroma_client.get_or_create_collection(name=collection_name)

    for i, chunk in enumerate(chunks):
        collection.add(
            ids=[f"chunk_{i}"],
            embeddings=[chunk["embedding"]],
            documents=[chunk["content"]],
            metadatas=[{
                "page": chunk["page"],
                "type": chunk["type"]
            }]
        )

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