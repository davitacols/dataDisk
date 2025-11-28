# API Quick Start Guide

Get started with the dataDisk Healthcare API in 5 minutes.

## Installation

```bash
pip install dataDisk flask requests
```

## Start the Server

```bash
python -m dataDisk.api
```

Server runs on `http://localhost:5000`

## Test the API

### 1. Health Check

```bash
curl http://localhost:5000/api/v1/health
```

Expected response:
```json
{"status": "healthy", "version": "1.0.0"}
```

### 2. De-identify a File

```bash
curl -X POST http://localhost:5000/api/v1/deidentify \
  -F "file=@patient_data.csv" \
  -F "method=safe_harbor"
```

Expected response:
```json
{
  "job_id": "abc123...",
  "status": "completed",
  "records_processed": 1000,
  "risk_score": {
    "overall_risk": "LOW",
    "k_anonymity": 15
  },
  "download_url": "/api/v1/download/abc123..."
}
```

### 3. Download Result

```bash
curl http://localhost:5000/api/v1/download/abc123... -o deidentified.csv
```

## Python Client

```python
import requests

API_URL = "http://localhost:5000/api/v1"

# Upload and process
with open('patient_data.csv', 'rb') as f:
    response = requests.post(
        f"{API_URL}/deidentify",
        files={'file': f},
        data={'method': 'safe_harbor'}
    )

job = response.json()
print(f"Job ID: {job['job_id']}")
print(f"Risk: {job['risk_score']['overall_risk']}")

# Download result
result = requests.get(f"{API_URL}/download/{job['job_id']}")
with open('deidentified.csv', 'wb') as f:
    f.write(result.content)

print("Done!")
```

## Custom Rules

```python
import json

rules = [
    {'column': 'ssn', 'pattern': r'\d{3}-\d{2}-\d{4}', 'action': 'redact'},
    {'column': 'phone', 'action': 'mask'},
    {'column': 'email', 'action': 'hash'}
]

with open('data.csv', 'rb') as f:
    response = requests.post(
        f"{API_URL}/deidentify",
        files={'file': f},
        data={
            'method': 'custom',
            'custom_rules': json.dumps(rules)
        }
    )
```

## Batch Processing

```python
import os
from concurrent.futures import ThreadPoolExecutor

def process_file(filepath):
    with open(filepath, 'rb') as f:
        response = requests.post(
            f"{API_URL}/deidentify",
            files={'file': f},
            data={'method': 'safe_harbor'}
        )
    return response.json()

# Process all CSV files in parallel
files = [f for f in os.listdir('data/') if f.endswith('.csv')]

with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(process_file, files))

print(f"Processed {len(results)} files")
```

## Error Handling

```python
try:
    with open('data.csv', 'rb') as f:
        response = requests.post(f"{API_URL}/deidentify", files={'file': f})
    
    if response.status_code == 200:
        job = response.json()
        print(f"Success: {job['job_id']}")
    else:
        error = response.json()
        print(f"Error: {error['error']}")
        
except FileNotFoundError:
    print("File not found")
except requests.exceptions.ConnectionError:
    print("API server not running")
```

## Production Deployment

### Using Gunicorn (Linux/Mac)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 dataDisk.api:app
```

### Using Waitress (Windows)

```bash
pip install waitress
waitress-serve --host=0.0.0.0 --port=5000 dataDisk.api:app
```

### Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "dataDisk.api:app"]
```

```bash
docker build -t datadisk-api .
docker run -p 5000:5000 datadisk-api
```

## Rate Limiting

Professional tier: 100 requests/hour
Enterprise tier: Unlimited

Contact sales@datadisk.io to upgrade.

## Support

- Documentation: docs.datadisk.io/api
- Email: api-support@datadisk.io
- Status: status.datadisk.io
