
from django.urls import path
from .views import GenerateHTMLReport, GetHTMLReport, GeneratePDFReport, GetPDFReport

urlpatterns = [
    path('assignment/html', GenerateHTMLReport.as_view(), name='generate_html'),
    path('assignment/html/<str:task_id>', GetHTMLReport.as_view(), name='get_html_report'),
    path('assignment/pdf', GeneratePDFReport.as_view(), name='generate_pdf'),
    path('assignment/pdf/<str:task_id>', GetPDFReport.as_view(), name='get_pdf_report'),
]
