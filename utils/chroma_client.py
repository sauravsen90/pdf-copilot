import chromadb
from chromadb.config import Settings

_chroma_client = None

def get_chroma_client():
    global _chroma_client
    if _chroma_client is None:
        _chroma_client = chromadb.Client(Settings(
            persist_directory="chroma_store",
            anonymized_telemetry=False
        ))
    return _chroma_client
