import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from report_generator.tasks import generate_html_report

# Test data
test_data = [
    {
        'student_id': 'test123',
        'events': [
            {'unit': '1', 'created_time': '2023-01-01T00:00:00Z'},
            {'unit': '2', 'created_time': '2023-01-02T00:00:00Z'},
        ],
        'namespace': 'test'
    }
]

# Call the task
result = generate_html_report.delay(test_data)
print(f"Task ID: {result.id}")
print(f"Task status: {result.status}")
print("Task submitted successfully!")
