# New Features: API, Custom Rules, and Risk Scoring

## Overview
Three powerful new features have been added to dataDisk Healthcare to enhance flexibility, automation, and compliance validation.

---

## 1. Batch Processing API

### What It Does
REST API for automated, programmatic de-identification of healthcare data. Perfect for integrating into existing workflows and processing large batches of files.

### Key Benefits
- **Automation**: Schedule recurring de-identification jobs
- **Integration**: Connect to EHR systems, data warehouses, ETL pipelines
- **Scalability**: Process multiple files simultaneously
- **Tracking**: Job status monitoring and audit trails

### Quick Start

#### Start the API Server
```bash
python -m dataDisk.api
```

Server runs on `http://localhost:5000`

#### Basic Usage
```python
import requests

# Upload and de-identify file
with open('patient_data.csv', 'rb') as f:
    response = requests.post(
        'http://localhost:5000/api/v1/deidentify',
        files={'file': f},
        data={'method': 'safe_harbor'}
    )

job = response.json()
print(f"Job ID: {job['job_id']}")
print(f"Risk Score: {job['risk_score']['overall_risk']}")

# Download result
result = requests.get(f"http://localhost:5000/api/v1/download/{job['job_id']}")
with open('deidentified.csv', 'wb') as f:
    f.write(result.content)
```

### API Endpoints

#### POST /api/v1/deidentify
De-identify uploaded file

**Parameters:**
- `file`: CSV or Excel file (required)
- `method`: 'safe_harbor', 'phi_removal', or 'custom' (default: 'safe_harbor')
- `custom_rules`: JSON array of custom rules (for method='custom')

**Response:**
```json
{
  "job_id": "uuid",
  "status": "completed",
  "records_processed": 1000,
  "risk_score": {
    "overall_risk": "LOW",
    "k_anonymity": 15
  },
  "download_url": "/api/v1/download/uuid"
}
```

#### GET /api/v1/status/{job_id}
Check job status

**Response:**
```json
{
  "status": "completed",
  "created_at": "2024-01-15T10:30:00",
  "records_processed": 1000,
  "method": "safe_harbor",
  "risk_score": {...}
}
```

#### GET /api/v1/download/{job_id}
Download de-identified file

Returns file as attachment

#### GET /api/v1/health
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### Use Cases

**1. Automated Nightly Processing**
```python
import schedule
import requests

def deidentify_daily_exports():
    files = ['export_monday.csv', 'export_tuesday.csv']
    for file in files:
        with open(file, 'rb') as f:
            requests.post('http://localhost:5000/api/v1/deidentify', 
                         files={'file': f})

schedule.every().day.at("02:00").do(deidentify_daily_exports)
```

**2. EHR Integration**
```python
# Pull data from EHR, de-identify, push to research database
ehr_data = pull_from_ehr()
ehr_data.to_csv('temp.csv')

with open('temp.csv', 'rb') as f:
    response = requests.post(API_URL, files={'file': f})
    
job_id = response.json()['job_id']
deidentified = requests.get(f"{API_URL}/download/{job_id}")

push_to_research_db(deidentified.content)
```

**3. Batch Processing**
```python
import os
import concurrent.futures

def process_file(filepath):
    with open(filepath, 'rb') as f:
        return requests.post(API_URL, files={'file': f})

files = [f for f in os.listdir('data/') if f.endswith('.csv')]

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    results = executor.map(process_file, files)
```

---

## 2. Custom Rules Engine

### What It Does
Define your own de-identification rules for flexible, organization-specific data protection. Go beyond standard HIPAA requirements.

### Key Benefits
- **Flexibility**: Handle custom PHI patterns unique to your organization
- **Control**: Choose exactly what to redact, mask, hash, or remove
- **Compliance**: Meet industry-specific regulations (GDPR, CCPA, etc.)
- **Reusability**: Save rule sets for consistent processing

### Rule Actions

| Action | Description | Example |
|--------|-------------|---------|
| `redact` | Replace with [REDACTED] | SSN → [REDACTED] |
| `mask` | Show last 4 characters | 1234-5678-9012 → ****-****-9012 |
| `hash` | One-way hash for linkage | john@email.com → a3f5b8c9d2e1f4a7 |
| `remove` | Delete column entirely | Drop 'photo' column |

### Quick Start

```python
from dataDisk.healthcare import HealthcareTransformation

# Define custom rules
rules = [
    {'column': 'ssn', 'pattern': r'\d{3}-\d{2}-\d{4}', 'action': 'redact'},
    {'column': 'phone', 'action': 'mask'},
    {'column': 'email', 'action': 'hash'},
    {'column': 'photo', 'action': 'remove'}
]

# Apply rules
result = HealthcareTransformation.apply_custom_rules(data, rules)
```

### Use Cases

**1. Financial Healthcare Data**
```python
# Protect both PHI and financial information
rules = [
    # Standard PHI
    {'column': 'ssn', 'action': 'redact'},
    {'column': 'name', 'action': 'remove'},
    
    # Financial data
    {'column': 'credit_card', 'pattern': r'\d{4}-\d{4}-\d{4}-\d{4}', 'action': 'mask'},
    {'column': 'bank_account', 'action': 'hash'},
    {'column': 'billing_address', 'action': 'remove'}
]
```

**2. Research Data Linkage**
```python
# Keep hashed identifiers for linking across datasets
rules = [
    {'column': 'patient_id', 'action': 'hash'},  # Keep for linkage
    {'column': 'email', 'action': 'hash'},       # Keep for linkage
    {'column': 'name', 'action': 'remove'},      # Remove direct identifier
    {'column': 'address', 'action': 'remove'}    # Remove direct identifier
]
```

**3. Multi-language PHI Detection**
```python
# Custom patterns for international data
rules = [
    # US SSN
    {'column': 'notes', 'pattern': r'\d{3}-\d{2}-\d{4}', 'action': 'redact'},
    
    # UK National Insurance Number
    {'column': 'notes', 'pattern': r'[A-Z]{2}\d{6}[A-Z]', 'action': 'redact'},
    
    # Canadian SIN
    {'column': 'notes', 'pattern': r'\d{3}-\d{3}-\d{3}', 'action': 'redact'}
]
```

**4. Free-text Note Scrubbing**
```python
# Remove PHI from clinical notes
rules = [
    {'column': 'clinical_notes', 'pattern': r'\d{3}-\d{2}-\d{4}', 'action': 'redact'},  # SSN
    {'column': 'clinical_notes', 'pattern': r'\d{3}-\d{3}-\d{4}', 'action': 'redact'},  # Phone
    {'column': 'clinical_notes', 'pattern': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', 'action': 'redact'},  # Email
    {'column': 'clinical_notes', 'pattern': r'\d{5}(-\d{4})?', 'action': 'redact'}  # ZIP
]
```

### API Integration

```python
# Use custom rules via API
import requests
import json

rules = [
    {'column': 'ssn', 'action': 'redact'},
    {'column': 'email', 'action': 'hash'}
]

with open('data.csv', 'rb') as f:
    response = requests.post(
        'http://localhost:5000/api/v1/deidentify',
        files={'file': f},
        data={
            'method': 'custom',
            'custom_rules': json.dumps(rules)
        }
    )
```

---

## 3. Re-identification Risk Score

### What It Does
Calculates the risk of re-identifying individuals in your de-identified dataset using k-anonymity and quasi-identifier analysis.

### Key Benefits
- **Validation**: Verify de-identification effectiveness
- **Compliance**: Demonstrate due diligence to auditors
- **Optimization**: Identify which fields need more generalization
- **Confidence**: Know your data is truly anonymous

### Risk Levels

| Level | K-Anonymity | Meaning |
|-------|-------------|---------|
| **LOW** | ≥10 | Safe for most uses |
| **MEDIUM** | 5-9 | Acceptable with caution |
| **HIGH** | <5 | Needs more de-identification |

### Quick Start

```python
from dataDisk.healthcare import HealthcareTransformation

# De-identify data
deidentified = HealthcareTransformation.safe_harbor_deidentification(data)

# Calculate risk
risk = HealthcareTransformation.calculate_reidentification_risk(deidentified)

print(f"Risk Level: {risk['overall_risk']}")
print(f"K-Anonymity: {risk['k_anonymity']}")
print(f"Quasi-Identifiers: {risk['quasi_identifiers']}")

# Get detailed report
print(HealthcareTransformation.get_risk_summary(risk))
```

### What Gets Analyzed

**Quasi-Identifiers**: Attributes that could be combined to re-identify someone
- Age/age ranges
- Gender
- Geographic data (ZIP, city, state)
- Dates (admission, discharge)
- Rare diagnoses
- Occupation
- Ethnicity

**K-Anonymity**: Minimum group size for any combination of quasi-identifiers
- K=5 means every person is indistinguishable from at least 4 others
- Higher K = better privacy protection

**PHI Pattern Detection**: Scans for remaining identifiers
- SSN patterns
- Phone numbers
- Email addresses
- IP addresses
- Medical record numbers

### Example Output

```
Re-identification Risk Assessment
==================================================
Overall Risk Level: LOW
K-Anonymity Score: 15
Unique Combinations: 67
Quasi-Identifiers: age_range, gender, state

Recommendations:
1. K-anonymity = 15: Good privacy protection
2. No PHI patterns detected
```

### Use Cases

**1. Compliance Validation**
```python
# Verify data meets k≥5 requirement before sharing
risk = HealthcareTransformation.calculate_reidentification_risk(data)

if risk['k_anonymity'] < 5:
    print("FAIL: Does not meet minimum k-anonymity")
    print("Recommendations:", risk['recommendations'])
else:
    print("PASS: Safe to share")
```

**2. Iterative De-identification**
```python
# Keep generalizing until risk is acceptable
data = original_data.copy()

while True:
    deidentified = HealthcareTransformation.safe_harbor_deidentification(data)
    risk = HealthcareTransformation.calculate_reidentification_risk(deidentified)
    
    if risk['overall_risk'] == 'LOW':
        break
    
    # Apply more aggressive generalization
    data = generalize_further(data)

print("Achieved LOW risk after optimization")
```

**3. Method Comparison**
```python
# Compare different de-identification approaches
methods = {
    'Basic': HealthcareTransformation.remove_phi(data),
    'Safe Harbor': HealthcareTransformation.safe_harbor_deidentification(data),
    'Custom': HealthcareTransformation.apply_custom_rules(data, aggressive_rules)
}

for name, result in methods.items():
    risk = HealthcareTransformation.calculate_reidentification_risk(result)
    print(f"{name}: Risk={risk['overall_risk']}, K={risk['k_anonymity']}")
```

**4. Audit Documentation**
```python
# Generate risk report for compliance audits
risk = HealthcareTransformation.calculate_reidentification_risk(data)
report = HealthcareTransformation.get_risk_summary(risk)

with open('compliance_report.txt', 'w') as f:
    f.write(report)
    f.write(f"\n\nProcessed: {datetime.now()}")
    f.write(f"\nRecords: {len(data)}")
    f.write(f"\nMethod: Safe Harbor")
```

### Web Interface

Risk scores are automatically displayed in the Streamlit app after de-identification:

- **Risk Level Badge**: Visual indicator (LOW/MEDIUM/HIGH)
- **K-Anonymity Metric**: Minimum group size
- **Unique Combinations**: Number of distinct quasi-identifier groups
- **Detailed Report**: Expandable section with recommendations

---

## Pricing Impact

These features are available across all tiers:

| Feature | Starter | Professional | Enterprise |
|---------|---------|--------------|------------|
| Custom Rules | ✓ Basic | ✓ Advanced | ✓ Unlimited |
| Risk Scoring | ✓ | ✓ | ✓ |
| API Access | - | ✓ | ✓ |
| API Rate Limit | - | 100 req/hour | Unlimited |

---

## Examples

See the `examples/` directory for complete working examples:

- `custom_rules_example.py` - 7 custom rule scenarios
- `api_example.py` - API integration patterns
- `risk_score_example.py` - Risk assessment workflows

---

## Next Steps

1. **Try the API**: `python -m dataDisk.api`
2. **Run Examples**: `python examples/custom_rules_example.py`
3. **Read API Docs**: See API reference for full endpoint documentation
4. **Contact Sales**: Upgrade to Professional for API access

---

## Support

- **Documentation**: docs.datadisk.io
- **Email**: support@datadisk.io
- **API Issues**: api-support@datadisk.io
