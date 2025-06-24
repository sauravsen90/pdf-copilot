from chromadb import PersistentClient
import os

def get_chroma_client():
    persist_dir = "chroma_store"

    if os.path.exists(persist_dir):
        print(f"[DEBUG] Chroma persist directory already exists: {persist_dir}")
    else:
        print(f"[DEBUG] Creating Chroma persist directory: {persist_dir}")

    chroma_client = PersistentClient(path=persist_dir)

    print(f"[DEBUG] Chroma client created with persistence at: {persist_dir}")
    print(f"[DEBUG] Chroma client type: {type(chroma_client)}")
    print(f"[DEBUG] Client has 'persist' method: {hasattr(chroma_client, 'persist')}")

    return chroma_client
