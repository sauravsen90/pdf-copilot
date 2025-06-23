📘 PDF Copilot

A FastAPI‑based RAG (Retrieval-Augmented Generation) assistant that reads a PDF manual, stores its content in a vector database, and answers user questions using Gemini.
🔧 Features

    PDF ingestion: Extracts paragraphs and tables using pdfplumber.

    Chunking: Splits the manual into manageable text blocks with metadata (page number, type).

    Embeddings: Generates vector embeddings via Gemini’s models/embedding-001.

    ChromaDB: Stores and retrieves chunks based on semantic similarity.

    Answer generation: Constructs grounded prompts using nearest chunks and generates answers with Gemini.

    FastAPI endpoint: Exposes the model through a /generate endpoint.

🧱 What’s Inside

pdf-copilot/
│
├── app/                          ← FastAPI web app (chat endpoint, etc.)
├── data/pdf/manual.pdf          ← Place your target PDF here
│
├── utils/
│   ├── pdf_loader.py            ← PDF → chunks
│   ├── embedding.py             ← Generates embeddings
│   ├── chroma.py                ← Save/query chunks in ChromaDB
│   └── rag.py                   ← RAG pipeline: retrieve + answer
│
├── test/                         ← Simple script-based tests
├── requirements.txt             ← Pip dependencies
└── .env                         ← Gemini API key and other secrets

⚙️ Quick Start (Local Use)

    Clone & install dependencies:

git clone https://github.com/sauravsen90/pdf-copilot.git
cd pdf-copilot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

Add your PDF:

    Place your car manual (e.g., TiagoBSVI_manual.pdf) in data/pdf/manual.pdf

Add your Gemini API Key:

echo 'GEMINI_API_KEY=your_key_here' > .env

Ingest and index PDF:

python -m test.index_pdf

This:

    Extracts chunks from data/pdf/manual.pdf

    Embeds them

    Saves them in ChromaDB

Test RAG response:

python -m test.generate_answers_with_rag

Sample query:
“What is the recommended tire pressure for Tiago?”

Run the API:

uvicorn app.main:app --reload

Then call via:

    curl -X POST http://localhost:8000/generate \
         -H 'Content-Type: application/json' \
         -d '{"query": "How often should I change the oil?"}'

📦 Directory Breakdown

    utils/pdf_loader.py
    Extracts paragraphs/tables with metadata from a PDF using pdfplumber.

    utils/embedding.py
    Encapsulates your embed_texts() method to embed chunk contents.

    utils/chroma.py
    Manages a ChromaDB singleton client and functions to store and retrieve chunks.

    utils/rag.py
    Retrieves top‑k relevant chunks and generates grounded answers via Gemini.

    app/
    FastAPI endpoints (e.g., /generate) implementing your copilot interface.

    test/
    Simple scripts for indexing and querying via CLI (python -m ...).

💡 Extensions You Might Consider

    OCR: Extract text from images (with pytesseract) and include them as chunks.

    Audio: Allow users to query via voice or support audio output.

    Follow-up prompts: Retain context for multi-step user conversation.

    Tabular support: Inject FAQs or captions for diagrams within the manual.

🛠️ Troubleshooting

    ChromaDB conflicts: Restart the server/session to reset in-memory state.

    Embedding errors: Confirm your .env is loaded and Gemini key is valid.

    Slow responses: Tune top_k in generate_answer_with_rag().

📚 Credits & License

    Gemini via google.generativeai for embeddings and text generation.

    ChromaDB for local vector storage and retrieval.

    pdfplumber for robust PDF parsing.

    FastAPI + Uvicorn for the web interface.
