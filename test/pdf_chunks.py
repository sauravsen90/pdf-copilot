from utils.pdf_loader import extract_pdf_chunks

chunks = extract_pdf_chunks("data/tiago_manual.pdf")
print(len(chunks), "pages_extracted")
print(chunks[0])