import pdfplumber
from django.core.files.uploadedfile import UploadedFile

def extract_text_from_pdf(pdf_file):
    """
    Handles both file paths and Django UploadedFile objects
    Returns: Extracted text with page separation markers
    """
    all_text = []
    
    with pdfplumber.open(pdf_file) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                all_text.append(f"=== PAGE {i+1} ===\n{text}")
    
    return "\n".join(all_text)

# enhancement for tabular data
def extract_tables_from_pdf(pdf_file):
    tables = []
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            tables.extend(page.extract_tables())
    return tables