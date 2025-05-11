from celery import shared_task
from .models import StudentReport
from io import BytesIO
from reportlab.pdfgen import canvas

# @shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
# def generate_html_report(self, data):
#     """
#     Generate HTML reports for multiple students.
#     """
#     results = []

#     for student in data:
#         try:
#             student_id = student['student_id']
#             events = student['events']
#             namespace = student.get('namespace', '')

#             # Sort events by created_time
#             events.sort(key=lambda x: x['created_time'])

#             # Generate Q-labels per unique unit
#             unique_units = sorted(set(int(e['unit']) for e in events))
#             unit_to_q = {unit: f"Q{idx+1}" for idx, unit in enumerate(unique_units)}

#             event_order = " -> ".join([unit_to_q[int(e['unit'])] for e in events])
#             html = f"<h2>Student ID: {student_id}</h2><p>Event Order: {event_order}</p>"

#             StudentReport.objects.update_or_create(
#                 student_id=student_id,
#                 report_type="html",
#                 defaults={
#                     "html_content": html,
#                     "task_id": self.request.id,
#                     "namespace": namespace,
#                 },
#             )

#             results.append({"student_id": student_id, "status": "completed"})
#         except Exception as e:
#             results.append({"student_id": student_id, "status": "failed", "error": str(e)})

#     return results


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def generate_html_report(self, data):
    results = []

    for student in data:
        try:
            student_id = student['student_id']
            events = student['events']
            namespace = student.get('namespace', '')

            events.sort(key=lambda x: x['created_time'])
            unique_units = sorted(set(int(e['unit']) for e in events))
            unit_to_q = {unit: f"Q{idx+1}" for idx, unit in enumerate(unique_units)}
            event_order = " -> ".join([unit_to_q[int(e['unit'])] for e in events])
            html = f"<h2>Student ID: {student_id}</h2><p>Event Order: {event_order}</p>"

            StudentReport.objects.update_or_create(
                student_id=student_id,
                namespace=namespace,
                defaults={
                    "html_content": html,
                    "html_task_id": self.request.id,
                },
            )

            results.append({"student_id": student_id, "status": "completed"})
        except Exception as e:
            results.append({"student_id": student_id, "status": "failed", "error": str(e)})

    return results



# @shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
# def generate_pdf_report(self, data):
#     """
#     Generate PDF reports for multiple students.
#     """
#     results = []

#     for student in data:
#         try:
#             student_id = student["student_id"]
#             events = student["events"]
#             namespace = student.get('namespace', '')

#             # Sort events and assign Q-labels
#             events.sort(key=lambda x: x['created_time'])
#             unique_units = sorted(set(int(e["unit"]) for e in events))
#             unit_to_q = {unit: f"Q{idx+1}" for idx, unit in enumerate(unique_units)}

#             event_order = " -> ".join([unit_to_q[int(e["unit"])] for e in events])

#             # Create PDF
#             buffer = BytesIO()
#             p = canvas.Canvas(buffer)
#             p.drawString(100, 800, f"Student ID: {student_id}")
#             p.drawString(100, 780, f"Event Order: {event_order}")
#             p.showPage()
#             p.save()
#             buffer.seek(0)
#             pdf_data = buffer.read()

#             StudentReport.objects.update_or_create(
#                 student_id=student_id,
#                 report_type="pdf",
#                 defaults={
#                     "pdf_file": pdf_data,
#                     "task_id": self.request.id,
#                     "namespace": namespace,
#                 },
#             )

#             results.append({"student_id": student_id, "status": "completed"})
#         except Exception as e:
#             results.append({"student_id": student_id, "status": "failed", "error": str(e)})

#     return results


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def generate_pdf_report(self, data):
    results = []

    for student in data:
        try:
            student_id = student["student_id"]
            events = student["events"]
            namespace = student.get("namespace", "")

            events.sort(key=lambda x: x['created_time'])
            unique_units = sorted(set(int(e["unit"]) for e in events))
            unit_to_q = {unit: f"Q{idx+1}" for idx, unit in enumerate(unique_units)}
            event_order = " -> ".join([unit_to_q[int(e["unit"])] for e in events])

            from io import BytesIO
            from reportlab.pdfgen import canvas
            buffer = BytesIO()
            p = canvas.Canvas(buffer)
            p.drawString(100, 800, f"Student ID: {student_id}")
            p.drawString(100, 780, f"Event Order: {event_order}")
            p.showPage()
            p.save()
            buffer.seek(0)
            pdf_data = buffer.read()

            StudentReport.objects.update_or_create(
                student_id=student_id,
                namespace=namespace,
                defaults={
                    "pdf_file": pdf_data,
                    "pdf_task_id": self.request.id,
                },
            )

            results.append({"student_id": student_id, "status": "completed"})
        except Exception as e:
            results.append({"student_id": student_id, "status": "failed", "error": str(e)})

    return results
