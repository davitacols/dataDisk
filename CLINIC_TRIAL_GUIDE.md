# 🏥 Clinic Trial Guide

## What You'll Test

✅ **De-identify your patient data** (CSV/Excel)  
✅ **Verify HIPAA compliance** (automatic validation)  
✅ **Generate audit logs** (required for compliance)  
✅ **See time/cost savings** (vs manual process)

---

## 3 Ways to Test

### Option 1: Web Interface (Recommended)
**Best for:** Non-technical users

```bash
streamlit run app_healthcare.py
```

Then:
1. Upload your CSV/Excel file
2. Click "De-identify Data"
3. Download results + audit log

**Time:** 2 minutes

---

### Option 2: Quick Test Script
**Best for:** Testing with your own data

```bash
python clinic_test.py
```

Follow prompts:
- Enter path to your CSV file (or press Enter for demo)
- Review results in `test_deidentified.csv`
- Check audit log in `test_audit_log.csv`

**Time:** 1 minute

---

### Option 3: Command Line
**Best for:** Developers/IT staff

```python
from dataDisk.healthcare import HealthcareTransformation
import pandas as pd

# Load your data
data = pd.read_csv('your_patient_data.csv')

# De-identify (one line!)
result = HealthcareTransformation.safe_harbor_deidentification(data)

# Save
result.to_csv('deidentified.csv', index=False)
```

**Time:** 30 seconds

---

## What Gets De-identified?

### Automatically Removed:
- ✅ Names (first, last, maiden)
- ✅ Addresses (street, city, ZIP)
- ✅ Phone numbers
- ✅ Email addresses
- ✅ SSN / Medical Record Numbers
- ✅ Dates (shifted randomly)
- ✅ Ages >89 (grouped as "90+")
- ✅ And 11 more HIPAA identifiers

### What Stays:
- ✅ Diagnosis codes
- ✅ Lab results
- ✅ Medications
- ✅ Clinical data
- ✅ State (geographic data at state level is OK)

---

## Sample Test Data

Don't have data ready? Use our sample:

```csv
patient_id,first_name,last_name,ssn,dob,diagnosis,age
P001,John,Doe,123-45-6789,1980-05-15,Diabetes,43
P002,Jane,Smith,987-65-4321,1975-08-22,Hypertension,48
P003,Bob,Johnson,555-12-3456,1990-12-01,Asthma,33
```

Save as `test_patients.csv` and run:
```bash
python clinic_test.py
```

---

## What You'll Get

### 1. De-identified Data
```csv
patient_id,first_name,last_name,ssn,dob,diagnosis,age_range
P001,[REDACTED],[REDACTED],[REDACTED],2024-04-25,Diabetes,40-49
P002,[REDACTED],[REDACTED],[REDACTED],2024-04-26,Hypertension,40-49
P003,[REDACTED],[REDACTED],[REDACTED],2024-04-27,Asthma,30-39
```

### 2. Compliance Report
```
✓ HIPAA COMPLIANT
- All 18 identifiers removed
- Ages >89 grouped
- Dates shifted
- Audit trail generated
```

### 3. Audit Log
```csv
timestamp,user,operation,record_count,data_hash
2024-01-15 10:30:00,clinic_test,de-identification,3,a9946ef34656
```

---

## Trial Checklist

Use this during your trial:

### Day 1: Setup (5 minutes)
- [ ] Install: `pip install -r requirements_healthcare.txt`
- [ ] Test with demo data: `python clinic_test.py`
- [ ] Verify it works

### Day 2: Your Data (15 minutes)
- [ ] Export patient data to CSV
- [ ] Run de-identification
- [ ] Compare before/after
- [ ] Verify PHI is removed

### Day 3: Validation (10 minutes)
- [ ] Check compliance report
- [ ] Review audit log
- [ ] Calculate time saved
- [ ] Calculate cost saved

### Day 4: Integration (30 minutes)
- [ ] Test with larger dataset (1,000+ records)
- [ ] Measure processing time
- [ ] Test with your team
- [ ] Document workflow

### Day 5: Decision
- [ ] Did it save 5+ hours?
- [ ] Is data HIPAA compliant?
- [ ] Easy enough for staff to use?
- [ ] Worth $299/month?

---

## Common Questions

### Q: What if I don't have Python installed?
**A:** Use the web interface - no coding required. Or we can provide a hosted trial.

### Q: Can I test with real patient data?
**A:** Yes! All processing happens locally on your computer. Data never leaves your system.

### Q: How long does processing take?
**A:** 
- 100 records: <5 seconds
- 1,000 records: <30 seconds
- 10,000 records: <5 minutes

### Q: What if I need help?
**A:** Email support@datadisk.io or schedule a call. We provide white-glove onboarding for trials.

### Q: Can I test specific features?
**A:** Yes! Tell us what you need:
- HL7 message parsing
- Database integration
- API access
- Custom transformations

### Q: What happens after the trial?
**A:** 
- Like it? Start at $99/month (beta pricing)
- Need changes? We'll customize it
- Not a fit? No problem, no commitment

---

## ROI Calculator

Calculate your savings:

**Current Process:**
- Time per dataset: ___ hours
- Hourly rate: $___
- Datasets per month: ___
- **Monthly cost: $___**

**With dataDisk:**
- Time per dataset: 0.1 hours (5 min)
- Monthly cost: $299
- **Monthly savings: $___**

**Example:**
- Current: 10 hours × $50/hour × 2 datasets = $1,000/month
- With dataDisk: $299/month
- **Savings: $701/month ($8,412/year)**

---

## Support During Trial

We're here to help:

📧 **Email:** support@datadisk.io  
📞 **Call:** Schedule at [calendly.com/datadisk]  
💬 **Chat:** Available in web app  
📚 **Docs:** See QUICKSTART_HEALTHCARE.md

**Response time:** <2 hours during business hours

---

## Ready to Start?

### Quick Start:
```bash
# 1. Install
pip install -r requirements_healthcare.txt

# 2. Test
python clinic_test.py

# 3. Review results
# Check test_deidentified.csv and test_audit_log.csv
```

### Need Help?
Email support@datadisk.io with:
- Your clinic name
- Number of records you process monthly
- Current de-identification process
- Best time for a demo call

We'll get you set up in 24 hours.

---

## Beta Offer

**First 10 clinics get:**
- ✅ $99/month (67% off forever)
- ✅ White-glove onboarding
- ✅ Priority support
- ✅ Feature requests prioritized
- ✅ Lock in price forever

**Limited spots available.**

Start trial: support@datadisk.io
