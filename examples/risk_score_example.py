"""
Example: Re-identification Risk Scoring with K-Anonymity
"""

import pandas as pd
from dataDisk.healthcare import HealthcareTransformation

# Create sample dataset with varying levels of identifiability
data = pd.DataFrame({
    'age': [25, 25, 25, 30, 30, 35, 35, 35, 35, 40],
    'gender': ['M', 'M', 'F', 'M', 'F', 'M', 'M', 'F', 'F', 'M'],
    'zip_code': ['10001', '10001', '10002', '10001', '10002', '10003', '10003', '10003', '10004', '10005'],
    'diagnosis': ['Diabetes', 'Hypertension', 'Asthma', 'Diabetes', 'Asthma', 
                  'Hypertension', 'Diabetes', 'Asthma', 'Diabetes', 'Hypertension']
})

print("Example 1: Calculate risk for quasi-identifiers")
print("="*80)
print("\nOriginal dataset:")
print(data)
print("\n")

# Calculate risk
risk = HealthcareTransformation.calculate_reidentification_risk(data)
print(HealthcareTransformation.get_risk_summary(risk))
print("\n")

# Example 2: High risk dataset (unique combinations)
print("\nExample 2: High Risk Dataset (Many Unique Combinations)")
print("="*80)

high_risk_data = pd.DataFrame({
    'age': [25, 26, 27, 28, 29, 30, 31, 32, 33, 34],
    'gender': ['M', 'F', 'M', 'F', 'M', 'F', 'M', 'F', 'M', 'F'],
    'zip_code': ['10001', '10002', '10003', '10004', '10005', 
                 '10006', '10007', '10008', '10009', '10010'],
    'diagnosis': ['Diabetes', 'Hypertension', 'Asthma', 'Diabetes', 'Asthma',
                  'Hypertension', 'Diabetes', 'Asthma', 'Diabetes', 'Hypertension']
})

print("\nHigh risk dataset (each person is unique):")
print(high_risk_data)
print("\n")

risk = HealthcareTransformation.calculate_reidentification_risk(high_risk_data)
print(HealthcareTransformation.get_risk_summary(risk))
print("\n")

# Example 3: Low risk dataset (generalized data)
print("\nExample 3: Low Risk Dataset (Generalized Data)")
print("="*80)

low_risk_data = pd.DataFrame({
    'age_range': ['20-30'] * 5 + ['30-40'] * 5,
    'gender': ['M', 'M', 'F', 'F', 'M', 'M', 'F', 'F', 'M', 'F'],
    'state': ['NY'] * 10,  # Only state-level geography
    'diagnosis': ['Diabetes', 'Hypertension', 'Asthma', 'Diabetes', 'Asthma',
                  'Hypertension', 'Diabetes', 'Asthma', 'Diabetes', 'Hypertension']
})

print("\nLow risk dataset (generalized attributes):")
print(low_risk_data)
print("\n")

risk = HealthcareTransformation.calculate_reidentification_risk(low_risk_data)
print(HealthcareTransformation.get_risk_summary(risk))
print("\n")

# Example 4: Improve risk by generalizing
print("\nExample 4: Reducing Risk Through Generalization")
print("="*80)

print("BEFORE generalization:")
print(high_risk_data)
risk_before = HealthcareTransformation.calculate_reidentification_risk(high_risk_data)
print(f"\nK-Anonymity: {risk_before['k_anonymity']}")
print(f"Risk Level: {risk_before['overall_risk']}")

# Generalize ages into ranges
high_risk_data['age_range'] = pd.cut(
    high_risk_data['age'],
    bins=[0, 30, 40, 100],
    labels=['<30', '30-40', '40+']
)
high_risk_data = high_risk_data.drop('age', axis=1)

# Generalize zip codes to first 3 digits
high_risk_data['zip_prefix'] = high_risk_data['zip_code'].str[:3]
high_risk_data = high_risk_data.drop('zip_code', axis=1)

print("\nAFTER generalization:")
print(high_risk_data)
risk_after = HealthcareTransformation.calculate_reidentification_risk(high_risk_data)
print(f"\nK-Anonymity: {risk_after['k_anonymity']}")
print(f"Risk Level: {risk_after['overall_risk']}")
print("\n")

# Example 5: Detect remaining PHI patterns
print("\nExample 5: Detecting Remaining PHI Patterns")
print("="*80)

data_with_phi = pd.DataFrame({
    'patient_id': ['P001', 'P002', 'P003'],
    'age_range': ['20-30', '30-40', '40-50'],
    'notes': ['Patient SSN: 123-45-6789', 'Contact: 555-123-4567', 'Normal checkup']
})

print("Dataset with hidden PHI:")
print(data_with_phi)
print("\n")

risk = HealthcareTransformation.calculate_reidentification_risk(data_with_phi)
print(HealthcareTransformation.get_risk_summary(risk))
print("\n")

# Example 6: Real-world scenario - 1000 patient records
print("\nExample 6: Large Dataset Risk Assessment")
print("="*80)

try:
    large_data = pd.read_csv('mock_patient_data_1000.csv')
    
    # De-identify using Safe Harbor
    deidentified = HealthcareTransformation.safe_harbor_deidentification(large_data)
    
    print(f"Original records: {len(large_data)}")
    print(f"Original columns: {len(large_data.columns)}")
    print(f"De-identified columns: {len(deidentified.columns)}")
    print("\n")
    
    # Calculate risk
    risk = HealthcareTransformation.calculate_reidentification_risk(deidentified)
    print(HealthcareTransformation.get_risk_summary(risk))
    
except FileNotFoundError:
    print("Large dataset not found. Run generate_mock_data.py first.")

print("\n")

# Example 7: Comparing different de-identification methods
print("\nExample 7: Risk Comparison Across Methods")
print("="*80)

sample_data = pd.DataFrame({
    'first_name': ['John', 'Jane', 'Bob', 'Alice', 'Charlie'],
    'last_name': ['Doe', 'Smith', 'Johnson', 'Williams', 'Brown'],
    'age': [25, 30, 35, 40, 45],
    'zip_code': ['10001', '10002', '10001', '10003', '10002'],
    'diagnosis': ['Diabetes', 'Hypertension', 'Asthma', 'Diabetes', 'Hypertension']
})

# Method 1: Basic PHI removal
method1 = HealthcareTransformation.remove_phi(sample_data.copy())
risk1 = HealthcareTransformation.calculate_reidentification_risk(method1)

# Method 2: Safe Harbor
method2 = HealthcareTransformation.safe_harbor_deidentification(sample_data.copy())
risk2 = HealthcareTransformation.calculate_reidentification_risk(method2)

# Method 3: Custom rules (more aggressive)
custom_rules = [
    {'column': 'first_name', 'action': 'remove'},
    {'column': 'last_name', 'action': 'remove'},
    {'column': 'zip_code', 'action': 'remove'}
]
method3 = HealthcareTransformation.apply_custom_rules(sample_data.copy(), custom_rules)
method3 = HealthcareTransformation.generalize_ages(method3)
risk3 = HealthcareTransformation.calculate_reidentification_risk(method3)

print("Method 1 (Basic PHI Removal):")
print(f"  Risk: {risk1['overall_risk']}, K-Anonymity: {risk1['k_anonymity']}")
print("\nMethod 2 (Safe Harbor):")
print(f"  Risk: {risk2['overall_risk']}, K-Anonymity: {risk2['k_anonymity']}")
print("\nMethod 3 (Custom Aggressive):")
print(f"  Risk: {risk3['overall_risk']}, K-Anonymity: {risk3['k_anonymity']}")
print("\nRecommendation: Use method with lowest risk for your use case")
