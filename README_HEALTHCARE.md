# 🏥 dataDisk Healthcare Edition

**HIPAA-Compliant Patient Data De-identification in Minutes**

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![HIPAA](https://img.shields.io/badge/HIPAA-Compliant-green.svg)](https://www.hhs.gov/hipaa)

## 🎯 Problem We Solve

Healthcare providers, researchers, and health tech companies need to share patient data for:
- Research collaborations
- Quality improvement initiatives  
- Analytics and reporting
- Third-party integrations

**But manual de-identification is:**
- ⏰ Time-consuming (10+ hours per dataset)
- 💸 Expensive (consultants charge $150-300/hour)
- ⚠️ Error-prone (human mistakes = HIPAA violations)
- 📋 Complex (18 identifiers to remove)

## ✨ Solution

dataDisk Healthcare Edition automates HIPAA-compliant de-identification:

✅ **10,000 records in <5 minutes** (vs 10+ hours manually)  
✅ **HIPAA Safe Harbor compliant** by default  
✅ **Audit logging** for all operations  
✅ **No coding required** - simple web interface  
✅ **Works offline** - your data never leaves your computer

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements_healthcare.txt

# Run the web app
streamlit run app_healthcare.py
```

### Command Line Usage

```python
from dataDisk.healthcare import HealthcareTransformation
import pandas as pd

# Load patient data
data = pd.read_csv('patient_data.csv')

# De-identify using HIPAA Safe Harbor method
deidentified = HealthcareTransformation.safe_harbor_deidentification(data)

# Validate compliance
report = HealthcareTransformation.validate_hipaa_compliance(deidentified)
print(f"Compliant: {report['compliant']}")

# Save results
deidentified.to_csv('deidentified_data.csv', index=False)
```

## 📋 Features

### HIPAA Safe Harbor De-identification
Automatically removes all 18 HIPAA identifiers:
- Names, addresses, phone numbers, emails
- SSN, medical record numbers, account numbers
- Dates (shifted randomly to preserve intervals)
- Ages >89 (grouped as "90+")
- Geographic subdivisions smaller than state
- And 9 more...

### Audit Logging
Track every operation for compliance:
- Who accessed the data
- What transformations were applied
- When the operation occurred
- Data hash for integrity verification

### Compliance Validation
Automatically check for:
- Direct identifiers (names, SSN, etc.)
- Ages >89 that need grouping
- Small cell sizes (<5 patients)
- Unmasked dates
- Geographic data

### HL7 Message Parsing
Parse and de-identify HL7 messages:
```python
from dataDisk.healthcare import HL7Parser

messages = ["MSH|^~\\&|LAB|Hospital...", ...]
parsed_data = HL7Parser.hl7_to_dataframe(messages)
deidentified = HealthcareTransformation.remove_phi(parsed_data)
```

### Patient Deduplication
Merge duplicate patient records:
```python
deduplicated = HealthcareTransformation.deduplicate_patients(
    data,
    match_columns=['first_name', 'last_name', 'dob']
)
```

## 📊 Examples

### Example 1: Basic De-identification
```python
from dataDisk.healthcare import HealthcareTransformation
import pandas as pd

data = pd.DataFrame({
    'patient_id': ['P001', 'P002'],
    'first_name': ['John', 'Jane'],
    'ssn': ['123-45-6789', '987-65-4321'],
    'diagnosis': ['Diabetes', 'Hypertension']
})

# Remove PHI
deidentified = HealthcareTransformation.remove_phi(data)
print(deidentified)
# Output:
#   patient_id  first_name         ssn     diagnosis
#   P001        [REDACTED]  [REDACTED]     Diabetes
#   P002        [REDACTED]  [REDACTED]  Hypertension
```

### Example 2: Complete Pipeline
```python
from dataDisk.pipeline import DataPipeline
from dataDisk.healthcare import HealthcareTransformation

pipeline = DataPipeline()

# Add transformation steps
pipeline.add_step(lambda df: HealthcareTransformation.create_patient_id(
    df, source_columns=['first_name', 'last_name', 'dob']
))
pipeline.add_step(lambda df: HealthcareTransformation.remove_phi(df))
pipeline.add_step(lambda df: HealthcareTransformation.generalize_ages(df))
pipeline.add_step(lambda df: HealthcareTransformation.mask_dates(df))

# Process data
result = pipeline.run(data)

# Generate audit log
audit = HealthcareTransformation.generate_audit_log(result, 'de-identification')
```

### Example 3: Web Interface
```bash
# Launch web app
streamlit run app_healthcare.py

# Then:
# 1. Upload CSV/Excel file
# 2. Select de-identification method
# 3. Click "De-identify Data"
# 4. Download results + audit log
```

## 💰 Pricing

### Starter - $299/month
- Up to 10,000 records/month
- Basic de-identification (Safe Harbor)
- CSV/Excel support
- Email support
- Audit logging

### Professional - $699/month
- Up to 100,000 records/month
- Advanced de-identification + HL7 parsing
- API access
- Database connectors (MySQL, PostgreSQL)
- Priority support
- Custom transformation rules

### Enterprise - $1,999/month
- Unlimited records
- On-premise deployment
- Custom integrations (Epic, Cerner, Allscripts)
- Dedicated account manager
- SLA guarantee
- Business Associate Agreement (BAA) included

[**Start Free Trial →**](https://datadisk.io/trial)

## 🔒 Security & Compliance

- **Local Processing**: All data processing happens on your computer. No data sent to cloud.
- **Audit Trails**: Complete logging of all operations for HIPAA compliance.
- **Safe Harbor Compliant**: Follows HIPAA Safe Harbor de-identification method.
- **BAA Available**: Business Associate Agreement for enterprise customers.
- **Open Source**: Code is auditable and transparent.

## 📚 Documentation

- [Full Documentation](https://docs.datadisk.io)
- [API Reference](https://docs.datadisk.io/api)
- [HIPAA Compliance Guide](https://docs.datadisk.io/hipaa)
- [Video Tutorials](https://youtube.com/datadisk)

## 🧪 Testing

```bash
# Run tests
pytest tests/test_healthcare.py -v

# Run example
python examples/healthcare_example.py
```

## 🤝 Support

- **Email**: support@datadisk.io
- **Documentation**: docs.datadisk.io
- **Issues**: github.com/davitacols/dataDisk/issues
- **Community**: Join our [Slack channel](https://datadisk.io/slack)

## ⚖️ Legal Disclaimer

This tool is provided as-is. Users are responsible for ensuring compliance with HIPAA and other applicable regulations. We recommend:

1. Consulting with legal counsel before production use
2. Conducting your own compliance review
3. Maintaining proper audit trails
4. Having a Business Associate Agreement in place

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

Built with:
- [pandas](https://pandas.pydata.org/) - Data manipulation
- [scikit-learn](https://scikit-learn.org/) - Machine learning transformations
- [Streamlit](https://streamlit.io/) - Web interface

---

**Made with ❤️ for Healthcare Professionals**

[Website](https://datadisk.io) | [Documentation](https://docs.datadisk.io) | [Twitter](https://twitter.com/datadisk)
