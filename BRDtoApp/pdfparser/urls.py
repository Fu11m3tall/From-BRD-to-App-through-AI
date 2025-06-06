# pdfparser/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_brd_view, name='upload_pdf'),
]

