"""
Test de-identification with 1000 patient records
"""

import pandas as pd
import time
from dataDisk.healthcare import HealthcareTransformation

print("="*60)
print("Testing dataDisk Healthcare with 1000 Records")
print("="*60)

# Load data
print("\n1. Loading 1000 patient records...")
data = pd.read_csv('mock_patient_data_1000.csv')
print(f"   Loaded: {len(data)} records, {len(data.columns)} columns")

# Show original data sample
print("\n2. Original data (first 3 records):")
print(data[['patient_id', 'first_name', 'last_name', 'ssn', 'age', 'diagnosis']].head(3))

# De-identify
print("\n3. De-identifying data...")
start_time = time.time()
deidentified = HealthcareTransformation.safe_harbor_deidentification(data)
end_time = time.time()

processing_time = end_time - start_time
print(f"   Processing time: {processing_time:.2f} seconds")
print(f"   Speed: {len(data)/processing_time:.0f} records/second")

# Show de-identified data
print("\n4. De-identified data (first 3 records):")
print(deidentified.head(3))

# Validate compliance
print("\n5. HIPAA Compliance Check...")
report = HealthcareTransformation.validate_hipaa_compliance(deidentified)
print(f"   Compliant: {report['compliant']}")
print(f"   Issues: {len(report['issues'])}")
print(f"   Warnings: {len(report['warnings'])}")

if report['issues']:
    print("\n   Issues found:")
    for issue in report['issues']:
        print(f"   - {issue}")

if report['warnings']:
    print("\n   Warnings:")
    for warning in report['warnings']:
        print(f"   - {warning}")

# Generate audit log
print("\n6. Generating audit log...")
audit = HealthcareTransformation.generate_audit_log(
    deidentified,
    operation='test_1000_records',
    user='test_user'
)

# Save results
print("\n7. Saving results...")
deidentified.to_csv('deidentified_1000.csv', index=False)
audit.to_csv('audit_1000.csv', index=False)
print("   Saved: deidentified_1000.csv")
print("   Saved: audit_1000.csv")

# Summary
print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print(f"Records processed: {len(data)}")
print(f"Processing time: {processing_time:.2f} seconds")
print(f"Columns before: {len(data.columns)}")
print(f"Columns after: {len(deidentified.columns)}")
print(f"PHI removed: {len(data.columns) - len(deidentified.columns)} columns")
print(f"HIPAA compliant: {'YES' if report['compliant'] else 'NO'}")
print(f"\nTime saved vs manual: ~{len(data) * 0.06:.1f} hours")
print(f"Cost saved (at $50/hour): ${len(data) * 0.06 * 50:.0f}")
print("="*60)
