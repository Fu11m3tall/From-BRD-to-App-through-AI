# pdfparser/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_and_parse_pdf, name='upload_pdf'),
]

