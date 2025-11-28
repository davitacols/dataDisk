# 🚀 Quick Start Guide - Healthcare Edition

Get started with dataDisk Healthcare in 5 minutes!

## Step 1: Installation (2 minutes)

```bash
# Clone or download the repository
cd dataDisk

# Install dependencies
pip install -r requirements_healthcare.txt
```

## Step 2: Run the Web App (1 minute)

```bash
# Launch the web interface
streamlit run app_healthcare.py
```

Your browser will open automatically at `http://localhost:8501`

## Step 3: De-identify Your First Dataset (2 minutes)

### Option A: Use Sample Data
1. Click "Load Sample Dataset" button
2. Click "🔒 De-identify Data"
3. Download the results

### Option B: Upload Your Data
1. Click "Upload CSV or Excel file"
2. Select your patient data file
3. Choose de-identification method (Safe Harbor recommended)
4. Click "🔒 De-identify Data"
5. Download de-identified data + audit log

## Step 4: Verify Compliance

1. Go to "📋 Compliance Check" tab
2. Review the compliance report
3. Download the report for your records

## 🎯 What Gets De-identified?

The HIPAA Safe Harbor method removes:

✅ **Names** - First, last, maiden names  
✅ **Addresses** - Street, city, ZIP codes  
✅ **Dates** - Birth dates, admission dates (shifted randomly)  
✅ **Phone Numbers** - All telephone numbers  
✅ **Email Addresses** - All email addresses  
✅ **SSN** - Social Security Numbers  
✅ **Medical Record Numbers** - MRN, account numbers  
✅ **Ages >89** - Grouped as "90+"  
✅ **And 10 more identifiers...**

## 📊 Example: Before & After

### Before (Original Data)
```
patient_id | first_name | last_name | ssn         | age | diagnosis
P001       | John       | Doe       | 123-45-6789 | 43  | Diabetes
P002       | Jane       | Smith     | 987-65-4321 | 95  | Hypertension
```

### After (De-identified)
```
patient_id | first_name | last_name | ssn        | age_range | diagnosis
P001       | [REDACTED] | [REDACTED]| [REDACTED] | 40-49     | Diabetes
P002       | [REDACTED] | [REDACTED]| [REDACTED] | 90+       | Hypertension
```

## 💻 Command Line Usage

For automation and scripting:

```python
from dataDisk.healthcare import HealthcareTransformation
import pandas as pd

# Load your data
data = pd.read_csv('patient_data.csv')

# De-identify (one line!)
deidentified = HealthcareTransformation.safe_harbor_deidentification(data)

# Save results
deidentified.to_csv('deidentified_data.csv', index=False)

# Validate compliance
report = HealthcareTransformation.validate_hipaa_compliance(deidentified)
print(f"HIPAA Compliant: {report['compliant']}")
```

## 🔧 Advanced Features

### Custom Pipeline
```python
from dataDisk.pipeline import DataPipeline
from dataDisk.healthcare import HealthcareTransformation

pipeline = DataPipeline()
pipeline.add_step(lambda df: HealthcareTransformation.create_patient_id(df, ['first_name', 'last_name', 'dob']))
pipeline.add_step(lambda df: HealthcareTransformation.remove_phi(df))
pipeline.add_step(lambda df: HealthcareTransformation.generalize_ages(df))

result = pipeline.run(data)
```

### HL7 Message Parsing
```python
from dataDisk.healthcare import HL7Parser

hl7_messages = [
    "MSH|^~\\&|LAB|Hospital|EMR|Clinic|20240115120000||ORU^R01|MSG001|P|2.5\nPID|1||P001||Doe^John||19800515|M",
    # ... more messages
]

parsed_data = HL7Parser.hl7_to_dataframe(hl7_messages)
deidentified = HealthcareTransformation.remove_phi(parsed_data)
```

### Patient Deduplication
```python
deduplicated = HealthcareTransformation.deduplicate_patients(
    data,
    match_columns=['first_name', 'last_name', 'dob']
)
```

## 📋 Compliance Checklist

Before using in production:

- [ ] Review your organization's HIPAA policies
- [ ] Consult with legal counsel
- [ ] Test with sample data first
- [ ] Verify all PHI is removed
- [ ] Keep audit logs for 6+ years
- [ ] Have a Business Associate Agreement (BAA) if needed
- [ ] Document your de-identification process
- [ ] Train staff on proper usage

## 🆘 Troubleshooting

### Issue: "Module not found" error
**Solution**: Install dependencies
```bash
pip install -r requirements_healthcare.txt
```

### Issue: "Cannot import HealthcareTransformation"
**Solution**: Make sure you're in the dataDisk directory
```bash
cd dataDisk
python -c "from dataDisk.healthcare import HealthcareTransformation; print('Success!')"
```

### Issue: Web app won't start
**Solution**: Check if port 8501 is available
```bash
streamlit run app_healthcare.py --server.port 8502
```

### Issue: Data not de-identifying correctly
**Solution**: Check your column names match PHI patterns
```python
# Print detected PHI columns
from dataDisk.healthcare import HealthcareTransformation
report = HealthcareTransformation.validate_hipaa_compliance(data)
print(report['issues'])
```

## 📞 Need Help?

- **Documentation**: See [README_HEALTHCARE.md](README_HEALTHCARE.md)
- **Examples**: Run `python examples/healthcare_example.py`
- **Support**: support@datadisk.io
- **Issues**: [GitHub Issues](https://github.com/davitacols/dataDisk/issues)

## 🎓 Next Steps

1. **Try the examples**: `python examples/healthcare_example.py`
2. **Read the full docs**: [README_HEALTHCARE.md](README_HEALTHCARE.md)
3. **Review pricing**: See [HEALTHCARE_MVP.md](HEALTHCARE_MVP.md)
4. **Schedule a demo**: support@datadisk.io

## 💰 Pricing

**Starter**: $299/month - Up to 10K records  
**Professional**: $699/month - Up to 100K records  
**Enterprise**: $1,999/month - Unlimited records

[**Start Free Trial →**](https://datadisk.io/trial)

---

**Questions?** Email support@datadisk.io or open an issue on GitHub.
