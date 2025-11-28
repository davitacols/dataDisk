"""
Example: Using Custom Rules Engine for flexible de-identification
"""

import pandas as pd
from dataDisk.healthcare import HealthcareTransformation

# Load sample data
data = pd.DataFrame({
    'patient_id': ['P001', 'P002', 'P003'],
    'first_name': ['John', 'Jane', 'Bob'],
    'last_name': ['Doe', 'Smith', 'Johnson'],
    'ssn': ['123-45-6789', '987-65-4321', '555-12-3456'],
    'phone': ['555-123-4567', '555-987-6543', '555-555-5555'],
    'email': ['john@email.com', 'jane@email.com', 'bob@email.com'],
    'credit_card': ['4532-1234-5678-9010', '5425-2345-6789-0123', '3782-8224-6310-005'],
    'diagnosis': ['Diabetes', 'Hypertension', 'Asthma'],
    'notes': ['Patient has SSN 123-45-6789 on file', 'Contact at 555-987-6543', 'Email: bob@email.com']
})

print("Original Data:")
print(data)
print("\n" + "="*80 + "\n")

# Example 1: Redact specific patterns
print("Example 1: Redact SSN patterns in all columns")
print("-" * 80)

rules = [
    {'column': 'ssn', 'pattern': r'\d{3}-\d{2}-\d{4}', 'action': 'redact'},
    {'column': 'notes', 'pattern': r'\d{3}-\d{2}-\d{4}', 'action': 'redact'}
]

result = HealthcareTransformation.apply_custom_rules(data.copy(), rules)
print(result[['ssn', 'notes']])
print("\n")

# Example 2: Mask sensitive data (show last 4 digits)
print("Example 2: Mask credit card numbers")
print("-" * 80)

rules = [
    {'column': 'credit_card', 'action': 'mask'}
]

result = HealthcareTransformation.apply_custom_rules(data.copy(), rules)
print(result[['patient_id', 'credit_card']])
print("\n")

# Example 3: Hash identifiers for linkage
print("Example 3: Hash identifiers for data linkage")
print("-" * 80)

rules = [
    {'column': 'patient_id', 'action': 'hash'},
    {'column': 'email', 'action': 'hash'}
]

result = HealthcareTransformation.apply_custom_rules(data.copy(), rules)
print(result[['patient_id', 'email']])
print("\n")

# Example 4: Remove columns entirely
print("Example 4: Remove sensitive columns")
print("-" * 80)

rules = [
    {'column': 'first_name', 'action': 'remove'},
    {'column': 'last_name', 'action': 'remove'},
    {'column': 'ssn', 'action': 'remove'}
]

result = HealthcareTransformation.apply_custom_rules(data.copy(), rules)
print("Remaining columns:", result.columns.tolist())
print(result)
print("\n")

# Example 5: Complex multi-step de-identification
print("Example 5: Complex multi-step de-identification")
print("-" * 80)

rules = [
    # Remove direct identifiers
    {'column': 'first_name', 'action': 'remove'},
    {'column': 'last_name', 'action': 'remove'},
    
    # Redact SSN patterns everywhere
    {'column': 'ssn', 'pattern': r'\d{3}-\d{2}-\d{4}', 'action': 'redact'},
    {'column': 'notes', 'pattern': r'\d{3}-\d{2}-\d{4}', 'action': 'redact'},
    
    # Mask phone numbers
    {'column': 'phone', 'action': 'mask'},
    {'column': 'notes', 'pattern': r'\d{3}-\d{3}-\d{4}', 'action': 'redact'},
    
    # Hash email for linkage
    {'column': 'email', 'action': 'hash'},
    {'column': 'notes', 'pattern': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', 'action': 'redact'},
    
    # Mask credit cards
    {'column': 'credit_card', 'action': 'mask'}
]

result = HealthcareTransformation.apply_custom_rules(data.copy(), rules)
print(result)
print("\n")

# Example 6: Industry-specific rules
print("Example 6: Industry-specific custom rules")
print("-" * 80)

# Healthcare research: Keep diagnosis, remove all identifiers
research_rules = [
    {'column': 'first_name', 'action': 'remove'},
    {'column': 'last_name', 'action': 'remove'},
    {'column': 'ssn', 'action': 'remove'},
    {'column': 'phone', 'action': 'remove'},
    {'column': 'email', 'action': 'remove'},
    {'column': 'credit_card', 'action': 'remove'},
    {'column': 'patient_id', 'action': 'hash'}  # Keep hashed ID for linkage
]

result = HealthcareTransformation.apply_custom_rules(data.copy(), research_rules)
print("Research dataset (diagnosis + hashed ID only):")
print(result)
print("\n")

# Example 7: Custom rules with validation
print("Example 7: Apply rules and validate risk")
print("-" * 80)

rules = [
    {'column': 'ssn', 'action': 'remove'},
    {'column': 'phone', 'action': 'mask'},
    {'column': 'email', 'action': 'hash'}
]

result = HealthcareTransformation.apply_custom_rules(data.copy(), rules)

# Calculate re-identification risk
risk_score = HealthcareTransformation.calculate_reidentification_risk(result)

print("De-identified data:")
print(result)
print("\n")
print("Risk Assessment:")
print(HealthcareTransformation.get_risk_summary(risk_score))
