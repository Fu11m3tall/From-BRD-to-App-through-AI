# pdfparser/views.py
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .utils import extract_text_from_pdf

def upload_and_parse_pdf(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(filename)
        parsed_text = extract_text_from_pdf(file_path)
        return render(request, 'pdfparser/upload_result.html', {
            'filename': uploaded_file.name,
            'parsed_text': parsed_text
        })
    return render(request, 'pdfparser/upload_result.html', {
        'error': 'No file uploaded.'
    })
