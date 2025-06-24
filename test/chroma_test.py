from utils.chroma import get_chroma_client

client = get_chroma_client()
collection = client.get_or_create_collection("tiago_manual")

print("🧮 Total chunks stored:", collection.count())

results = collection.query(query_texts=["engine"], n_results=5)
print("🔎 Example chunks:")
for doc in results["documents"][0]:
    print("-", doc[:100])