"""
Quick test script for clinics to try dataDisk Healthcare
Upload your own CSV file and see results in seconds
"""

import pandas as pd
from dataDisk.healthcare import HealthcareTransformation

print("=" * 60)
print("dataDisk Healthcare - Quick Test")
print("=" * 60)

# Step 1: Load your data
print("\n1. Loading your patient data...")
file_path = input("Enter path to your CSV file (or press Enter for demo): ").strip()

if not file_path:
    # Demo data
    data = pd.DataFrame({
        'patient_id': ['P001', 'P002', 'P003'],
        'first_name': ['John', 'Jane', 'Bob'],
        'last_name': ['Doe', 'Smith', 'Johnson'],
        'ssn': ['123-45-6789', '987-65-4321', '555-12-3456'],
        'dob': ['1980-05-15', '1975-08-22', '1990-12-01'],
        'phone': ['555-123-4567', '555-987-6543', '555-555-5555'],
        'email': ['john@email.com', 'jane@email.com', 'bob@email.com'],
        'age': [43, 48, 33],
        'diagnosis': ['Diabetes', 'Hypertension', 'Asthma']
    })
    print("✓ Using demo data (3 patients)")
else:
    data = pd.read_csv(file_path)
    print(f"✓ Loaded {len(data)} records from {file_path}")

print(f"\nOriginal columns: {', '.join(data.columns.tolist())}")

# Step 2: De-identify
print("\n2. De-identifying data (HIPAA Safe Harbor method)...")
deidentified = HealthcareTransformation.safe_harbor_deidentification(data)
print(f"✓ De-identification complete!")

# Step 3: Validate compliance
print("\n3. Validating HIPAA compliance...")
report = HealthcareTransformation.validate_hipaa_compliance(deidentified)

if report['compliant']:
    print("✓ HIPAA COMPLIANT - No issues found")
else:
    print("⚠ COMPLIANCE ISSUES:")
    for issue in report['issues']:
        print(f"  - {issue}")

if report['warnings']:
    print("\nWarnings:")
    for warning in report['warnings']:
        print(f"  - {warning}")

# Step 4: Generate audit log
print("\n4. Generating audit log...")
audit = HealthcareTransformation.generate_audit_log(
    deidentified,
    operation='test_de-identification',
    user='clinic_test'
)
print("✓ Audit log created")

# Step 5: Save results
print("\n5. Saving results...")
deidentified.to_csv('test_deidentified.csv', index=False)
audit.to_csv('test_audit_log.csv', index=False)
print("✓ Saved to:")
print("  - test_deidentified.csv")
print("  - test_audit_log.csv")

# Step 6: Show summary
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Records processed: {len(data)}")
print(f"Columns before: {len(data.columns)}")
print(f"Columns after: {len(deidentified.columns)}")
print(f"HIPAA compliant: {'YES' if report['compliant'] else 'NO'}")
print(f"Time saved: ~{len(data) * 0.06:.1f} hours (vs manual)")
print(f"Cost saved: ~${len(data) * 0.06 * 50:.0f} (at $50/hour)")

print("\n" + "=" * 60)
print("NEXT STEPS")
print("=" * 60)
print("1. Review test_deidentified.csv")
print("2. Check test_audit_log.csv")
print("3. Compare with your original data")
print("4. Ready to go live? Contact: support@datadisk.io")
print("\nQuestions? Run: streamlit run app_healthcare.py")
print("=" * 60)
