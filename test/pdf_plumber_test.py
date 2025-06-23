from utils.pdf_loader import extract_pdf_chunks

chunks = extract_pdf_chunks('data/tiago_manual.pdf')
                            
for chunk in chunks[:5]:
    print(f"[{chunk['type'].upper()}] Page {chunk['page']}")
    print(chunk["content"][:300])  # show first 300 characters
    print("-" * 80)    