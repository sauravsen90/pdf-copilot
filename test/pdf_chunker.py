from utils.pdf_loader import extract_pdf_chunks, chunk_text_blocks

pages = extract_pdf_chunks("data/tiago_manual.pdf")
chunked = chunk_text_blocks(pages, sentence_per_chunk=5)

print(f"Extracted {len(chunked)} chunks from {len(pages)} pages")
print(chunked[40])