"""
Example: Using the dataDisk Healthcare API for batch processing
"""

import requests
import json
import time

# API endpoint (adjust based on your deployment)
API_URL = "http://localhost:5000/api/v1"

def deidentify_file(file_path, method='safe_harbor', custom_rules=None):
    """
    De-identify a file using the API.
    
    Args:
        file_path: Path to CSV or Excel file
        method: 'safe_harbor', 'phi_removal', or 'custom'
        custom_rules: List of custom rules (for method='custom')
    
    Returns:
        Job ID for tracking
    """
    with open(file_path, 'rb') as f:
        files = {'file': f}
        data = {'method': method}
        
        if custom_rules:
            data['custom_rules'] = json.dumps(custom_rules)
        
        response = requests.post(f"{API_URL}/deidentify", files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"Job submitted: {result['job_id']}")
            print(f"Status: {result['status']}")
            print(f"Records processed: {result['records_processed']}")
            print(f"Risk score: {result['risk_score']['overall_risk']}")
            return result['job_id']
        else:
            print(f"Error: {response.json()}")
            return None


def check_status(job_id):
    """Check job status."""
    response = requests.get(f"{API_URL}/status/{job_id}")
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.json()}")
        return None


def download_result(job_id, output_path):
    """Download de-identified file."""
    response = requests.get(f"{API_URL}/download/{job_id}")
    
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded to: {output_path}")
        return True
    else:
        print(f"Error: {response.json()}")
        return False


# Example 1: Basic Safe Harbor de-identification
print("Example 1: Safe Harbor De-identification")
print("-" * 50)
job_id = deidentify_file('mock_patient_data_1000.csv', method='safe_harbor')

if job_id:
    # Check status
    status = check_status(job_id)
    print(f"\nJob status: {status['status']}")
    
    # Download result
    if status['status'] == 'completed':
        download_result(job_id, 'deidentified_output.csv')

print("\n")

# Example 2: Custom rules de-identification
print("Example 2: Custom Rules De-identification")
print("-" * 50)

custom_rules = [
    {'column': 'ssn', 'pattern': r'\d{3}-\d{2}-\d{4}', 'action': 'redact'},
    {'column': 'phone', 'pattern': r'\d{3}-\d{3}-\d{4}', 'action': 'mask'},
    {'column': 'email', 'action': 'hash'},
    {'column': 'address', 'action': 'remove'}
]

job_id = deidentify_file(
    'mock_patient_data_1000.csv',
    method='custom',
    custom_rules=custom_rules
)

if job_id:
    status = check_status(job_id)
    print(f"\nJob status: {status['status']}")
    print(f"Risk score: {status.get('risk_score', {})}")

print("\n")

# Example 3: Batch processing multiple files
print("Example 3: Batch Processing")
print("-" * 50)

files = ['file1.csv', 'file2.csv', 'file3.csv']
job_ids = []

for file_path in files:
    try:
        job_id = deidentify_file(file_path, method='safe_harbor')
        if job_id:
            job_ids.append(job_id)
    except FileNotFoundError:
        print(f"File not found: {file_path}")

# Wait for all jobs to complete
print(f"\nProcessing {len(job_ids)} files...")
time.sleep(2)

for job_id in job_ids:
    status = check_status(job_id)
    print(f"Job {job_id}: {status['status']}")

print("\n")

# Example 4: Health check
print("Example 4: API Health Check")
print("-" * 50)

response = requests.get(f"{API_URL}/health")
if response.status_code == 200:
    health = response.json()
    print(f"API Status: {health['status']}")
    print(f"Version: {health['version']}")
