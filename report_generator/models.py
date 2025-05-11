
from django.db import models

class StudentReport(models.Model):
    namespace = models.CharField(max_length=128, blank=True, null=True, db_index=True)
    student_id = models.CharField(max_length=64, db_index=True)

    # Store task IDs for tracking
    html_task_id = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    pdf_task_id = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    # Report content
    html_content = models.TextField(blank=True, null=True)
    pdf_file = models.BinaryField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("student_id", "namespace")
        indexes = [
            models.Index(fields=["student_id"]),
            models.Index(fields=["namespace"]),
        ]

    def __str__(self):
        return f"{self.student_id} ({self.namespace or 'default'})"
