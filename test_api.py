import requests
import time

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_html_report():
    print("Testing HTML Report Generation...")
    
    # Test data for HTML report
    data = [
        {
            'student_id': 'test123',
            'events': [
                {'unit': '1', 'created_time': '2023-01-01T00:00:00Z'},
                {'unit': '2', 'created_time': '2023-01-02T00:00:00Z'},
            ],
            'namespace': 'test'
        }
    ]
    
    # Send POST request to generate HTML report
    response = requests.post(f"{BASE_URL}/assignment/html", json=data)
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.text}")
    
    if response.status_code == 202:
        task_id = response.json().get('task_id')
        print(f"Task ID: {task_id}")
        
        # Poll for the result
        max_retries = 10
        for i in range(max_retries):
            response = requests.get(f"{BASE_URL}/assignment/html/{task_id}")
            result = response.json()
            print(f"Polling result (attempt {i+1}): {result}")
            
            if result.get('status') == 'completed':
                print("HTML Report Generation Test Passed!")
                print(f"Student ID: {result.get('student_id')}")
                print(f"HTML Content: {result.get('html')[:100]}...")  # Print first 100 chars
                return True
            elif result.get('status') == 'failed':
                print("HTML Report Generation Failed!")
                return False
                
            time.sleep(1)  # Wait 1 second before next poll
        
        print("Max retries reached. Task is taking too long.")
        return False
    
    print("Failed to start HTML report generation task.")
    return False

def test_pdf_report():
    print("\nTesting PDF Report Generation...")
    
    # Test data for PDF report
    data = [
        {
            'student_id': 'test123',
            'events': [
                {'unit': '1', 'created_time': '2023-01-01T00:00:00Z'},
                {'unit': '2', 'created_time': '2023-01-02T00:00:00Z'},
            ],
            'namespace': 'test'
        }
    ]
    
    # Send POST request to generate PDF report
    response = requests.post(f"{BASE_URL}/assignment/pdf", json=data)
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.text}")
    
    if response.status_code == 202:
        task_id = response.json().get('task_id')
        print(f"Task ID: {task_id}")
        
        # Poll for the result
        max_retries = 10
        for i in range(max_retries):
            response = requests.get(f"{BASE_URL}/assignment/pdf/{task_id}")
            
            # Check if the response is JSON (for pending/failed states) or a file download
            content_type = response.headers.get('content-type', '')
            
            if 'application/json' in content_type:
                # Handle JSON response (pending/failed states)
                result = response.json()
                print(f"Polling result (attempt {i+1}): {result}")
                
                if result.get('status') == 'pending':
                    # Continue polling
                    pass
                elif result.get('status') == 'failed':
                    print("PDF Report Generation Failed!")
                    return False
                else:
                    print(f"Unexpected JSON response: {result}")
                    return False
            elif 'application/pdf' in content_type:
                # Handle PDF file download
                print("PDF Report Generation Test Passed!")
                content_disposition = response.headers.get('content-disposition', '')
                filename = 'report.pdf'
                if 'filename=' in content_disposition:
                    filename = content_disposition.split('filename=')[1].strip('"\'')
                
                # Save the PDF file
                with open(filename, 'wb') as f:
                    f.write(response.content)
                
                print(f"PDF report saved as: {filename}")
                print(f"PDF size: {len(response.content)} bytes")
                return True
            else:
                print(f"Unexpected response content type: {content_type}")
                print(f"Response content: {response.text[:500]}...")
                return False
                
            time.sleep(1)  # Wait 1 second before next poll
        
        print("Max retries reached. Task is taking too long.")
        return False
    
    print("Failed to start PDF report generation task.")
    return False

if __name__ == "__main__":
    print("Starting API Tests...")
    print("======================")
    
    # Test HTML Report API
    html_success = test_html_report()
    
    # Test PDF Report API
    pdf_success = test_pdf_report()
    
    print("\nTest Summary:")
    print("=============")
    print(f"HTML Report Test: {'PASSED' if html_success else 'FAILED'}")
    print(f"PDF Report Test: {'PASSED' if pdf_success else 'FAILED'}")
