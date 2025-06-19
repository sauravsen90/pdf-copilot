import pdfplumber
from typing import List, Dict

def extract_pdf_chunks(path_to_pdf: str) -> List[Dict]:
    """
    Extract paragraphs and tables from PDF using pdfplumber.
    Returns list of {type: 'text' | 'table', content: ..., page: ...}
    """
    chunks=[]

    with pdfplumber.open(path_to_pdf) as pdf:
        for i in enumerate(pdf.pages):
            page_number = i+1

            # Extract plain text
            raw_text = page.extract_text()
            if raw_text:
                paragraphs = [p.strip() for p in raw_text.split("\n\n") if p.strip()]
                for para in paragraphs:
                    chunks.append(
                        {
                            "type": "text",
                            "content": para,
                            "page": page_number
                        }
                    )

            # Extract table and format
            tables = page.extract_tables()
            for table in tables:
                if table:
                    table_text = format_as_table_text(table)
                    chunks.append(
                        {
                            "type: "table"
                            "content": table_text,
                            "page": page_number
                        }
                    )

    return chunks

def format_table_as_text(table: List[List[str]]) -> str:
    """
    Convert a table (list of rows) into a plain text grid format.
    You could later improve this with markdown or CSV output.
    """
    formatted_rows = []
    col_widths = [max()for col in zip(*table)]    