from django.urls import path
from .views import test_pdf_parsing

urlpatterns = [
    path('test-pdf/', test_pdf_parsing, name='test_pdf'),
]
