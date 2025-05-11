from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from celery.result import AsyncResult
from .tasks import generate_html_report, generate_pdf_report
from .models import StudentReport


class GenerateHTMLReport(APIView):
    def post(self, request):
        task = generate_html_report.delay(request.data)
        return Response({"task_id": task.id}, status=status.HTTP_202_ACCEPTED)


class GetHTMLReport(APIView):
    def get(self, request, task_id):
        result = AsyncResult(task_id)
        if result.state == "PENDING":
            return Response({"status": "pending"})
        elif result.state == "SUCCESS":
            report = StudentReport.objects.filter(html_task_id=task_id).first()
            if not report or not report.html_content:
                return Response({"status": "failed"}, status=404)
            return Response({
                "status": "completed",
                "student_id": report.student_id,
                "html": report.html_content,
            })
        elif result.state == "FAILURE":
            return Response({"status": "failed"}, status=500)
        else:
            return Response({"status": result.state})





class GeneratePDFReport(APIView):
    def post(self, request):
        task = generate_pdf_report.delay(request.data)
        return Response({"task_id": task.id}, status=status.HTTP_202_ACCEPTED)


class GetPDFReport(APIView):
    def get(self, request, task_id):
        result = AsyncResult(task_id)
        if result.state == "PENDING":
            return Response({"status": "pending"})
        elif result.state == "SUCCESS":
            report = StudentReport.objects.filter(pdf_task_id=task_id).first()
            if not report or not report.pdf_file:
                return Response({"status": "failed"}, status=404)

            response = HttpResponse(report.pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{report.student_id}_report.pdf"'
            return response
        elif result.state == "FAILURE":
            return Response({"status": "failed"}, status=500)
        else:
            return Response({"status": result.state})
