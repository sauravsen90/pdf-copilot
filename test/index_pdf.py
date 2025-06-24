# test/index_pdf.py

from utils.pdf_loader import extract_pdf_chunks
from utils.embeddings import get_embeddings_from_chunks
from utils.chroma import save_chunks_to_chroma

def main():
    pdf_path = "data/tiago_manual.pdf"
    collection_name = "tiago_manual"

    print("Extracting chunks from PDF...")
    chunks = extract_pdf_chunks(pdf_path)
    # chunks = chunks[:10]
    print(f"Extracted {len(chunks)} chunks.")

    print("Embedding chunks via Gemini...")
    embedded_chunks = get_embeddings_from_chunks(chunks)
    print(f"Got embeddings for {len(embedded_chunks)} chunks.")

    print("Saving to ChromaDB...")
    save_chunks_to_chroma(embedded_chunks, collection_name)
    print(f"Saved {len(embedded_chunks)} chunks to Chroma collection '{collection_name}'.")

if __name__ == "__main__":
    main()
