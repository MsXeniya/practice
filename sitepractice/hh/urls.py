from django.urls import path
from .views import search_form, parse_resumes

urlpatterns = [
    path('', search_form, name='search_form'),
    path('parse_resumes/', parse_resumes, name='parse_resumes'),
]
