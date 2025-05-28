from django.shortcuts import render
from django.http import HttpResponse
from .utils import extract_text_from_pdf
import os

def test_pdf_parsing(request):
    # For testing, use a sample PDF stored in your project folder (e.g. inside 'media' folder)
    sample_pdf_path = os.path.join('media', 'sample_brd.pdf')

    text = extract_text_from_pdf(sample_pdf_path)
    return HttpResponse(f"<pre>{text}</pre>")
        
# Create your views here.
