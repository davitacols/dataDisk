"""
Healthcare data pipeline example demonstrating HIPAA-compliant transformations.
"""

import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dataDisk.pipeline import DataPipeline
from dataDisk.healthcare import HealthcareTransformation, HL7Parser
from dataDisk.data_sinks import CSVSink


def create_sample_patient_data():
    """Create sample patient data with PHI."""
    return pd.DataFrame({
        'patient_id': ['P001', 'P002', 'P003', 'P004', 'P005'],
        'first_name': ['John', 'Jane', 'Bob', 'Alice', 'Charlie'],
        'last_name': ['Doe', 'Smith', 'Johnson', 'Williams', 'Brown'],
        'ssn': ['123-45-6789', '987-65-4321', '555-12-3456', '111-22-3333', '999-88-7777'],
        'dob': ['1980-05-15', '1975-08-22', '1990-12-01', '1945-03-10', '1992-07-18'],
        'phone': ['555-123-4567', '555-987-6543', '555-555-5555', '555-111-2222', '555-999-8888'],
        'email': ['john@email.com', 'jane@email.com', 'bob@email.com', 'alice@email.com', 'charlie@email.com'],
        'address': ['123 Main St', '456 Oak Ave', '789 Pine Rd', '321 Elm St', '654 Maple Dr'],
        'city': ['Boston', 'New York', 'Chicago', 'Miami', 'Seattle'],
        'state': ['MA', 'NY', 'IL', 'FL', 'WA'],
        'zip': ['02101', '10001', '60601', '33101', '98101'],
        'age': [43, 48, 33, 78, 31],
        'diagnosis': ['Diabetes', 'Hypertension', 'Asthma', 'Arthritis', 'Diabetes'],
        'visit_date': ['2024-01-15', '2024-01-16', '2024-01-17', '2024-01-18', '2024-01-19'],
        'blood_pressure': ['120/80', '140/90', '110/70', '150/95', '118/78'],
        'weight_kg': [75.5, 68.2, 82.1, 65.0, 90.3]
    })


def example_1_basic_deidentification():
    """Example 1: Basic PHI removal."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic De-identification")
    print("="*60)
    
    # Create sample data
    data = create_sample_patient_data()
    print("\nOriginal data (first 2 rows):")
    print(data.head(2))
    
    # Remove PHI
    deidentified = HealthcareTransformation.remove_phi(data)
    print("\nDe-identified data (first 2 rows):")
    print(deidentified.head(2))
    
    # Save to file
    sink = CSVSink('deidentified_patients.csv')
    sink.save(deidentified)
    print("\n[SUCCESS] Saved to deidentified_patients.csv")


def example_2_safe_harbor_method():
    """Example 2: HIPAA Safe Harbor de-identification."""
    print("\n" + "="*60)
    print("EXAMPLE 2: HIPAA Safe Harbor De-identification")
    print("="*60)
    
    data = create_sample_patient_data()
    
    # Apply Safe Harbor method
    safe_data = HealthcareTransformation.safe_harbor_deidentification(data)
    print("\nSafe Harbor de-identified data:")
    print(safe_data.head())
    
    # Validate compliance
    report = HealthcareTransformation.validate_hipaa_compliance(safe_data)
    print("\nCompliance Report:")
    print(f"  Compliant: {report['compliant']}")
    print(f"  Issues: {report['issues'] if report['issues'] else 'None'}")
    print(f"  Warnings: {report['warnings'] if report['warnings'] else 'None'}")


def example_3_pipeline_with_audit():
    """Example 3: Complete pipeline with audit logging."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Pipeline with Audit Logging")
    print("="*60)
    
    data = create_sample_patient_data()
    
    # Create audit log for initial data access
    audit_log = HealthcareTransformation.generate_audit_log(
        data, 
        operation='read',
        user='data_analyst_1'
    )
    print("\nAudit Log Entry:")
    print(audit_log)
    
    # Create pipeline
    pipeline = DataPipeline()
    
    # Add transformation steps
    pipeline.add_step(lambda df: HealthcareTransformation.create_patient_id(
        df, 
        source_columns=['first_name', 'last_name', 'dob'],
        id_column='anonymous_id'
    ))
    pipeline.add_step(lambda df: HealthcareTransformation.remove_phi(df))
    pipeline.add_step(lambda df: HealthcareTransformation.generalize_ages(df))
    pipeline.add_step(lambda df: HealthcareTransformation.mask_dates(df, shift_days=100))
    
    # Process data
    result = pipeline.run(data)
    
    print("\nProcessed data:")
    print(result.head())
    
    # Generate final audit log
    final_audit = HealthcareTransformation.generate_audit_log(
        result,
        operation='transform_and_export',
        user='data_analyst_1'
    )
    
    # Save audit trail
    audit_trail = pd.concat([audit_log, final_audit], ignore_index=True)
    audit_sink = CSVSink('audit_trail.csv')
    audit_sink.save(audit_trail)
    print("\n[SUCCESS] Audit trail saved to audit_trail.csv")
    
    # Get pipeline metrics
    metrics = pipeline.get_metrics()
    print(f"\nPipeline execution time: {metrics['total_processing_time']:.4f}s")


def example_4_patient_deduplication():
    """Example 4: Patient record deduplication."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Patient Deduplication")
    print("="*60)
    
    # Create data with duplicates
    data = pd.DataFrame({
        'first_name': ['John', 'John', 'Jane', 'Jane', 'Bob'],
        'last_name': ['Doe', 'Doe', 'Smith', 'Smith', 'Johnson'],
        'dob': ['1980-05-15', '1980-05-15', '1975-08-22', '1975-08-22', '1990-12-01'],
        'mrn': ['MRN001', 'MRN002', 'MRN003', 'MRN004', 'MRN005'],
        'visit_date': ['2024-01-15', '2024-01-20', '2024-01-16', '2024-01-21', '2024-01-17']
    })
    
    print(f"\nOriginal records: {len(data)}")
    print(data)
    
    # Deduplicate
    deduplicated = HealthcareTransformation.deduplicate_patients(
        data,
        match_columns=['first_name', 'last_name', 'dob']
    )
    
    print(f"\nAfter deduplication: {len(deduplicated)}")
    print(deduplicated)


def example_5_hl7_parsing():
    """Example 5: Parse HL7 messages."""
    print("\n" + "="*60)
    print("EXAMPLE 5: HL7 Message Parsing")
    print("="*60)
    
    # Sample HL7 messages
    hl7_messages = [
        """MSH|^~\\&|LAB|Hospital|EMR|Clinic|20240115120000||ORU^R01|MSG001|P|2.5
PID|1||P001||Doe^John||19800515|M|||123 Main St^^Boston^MA^02101
OBX|1|NM|GLU^Glucose||95|mg/dL|70-100|N|||F""",
        
        """MSH|^~\\&|LAB|Hospital|EMR|Clinic|20240116130000||ORU^R01|MSG002|P|2.5
PID|1||P002||Smith^Jane||19750822|F|||456 Oak Ave^^New York^NY^10001
OBX|1|NM|BP^Blood Pressure||140/90|mmHg|<120/80|H|||F"""
    ]
    
    # Parse HL7 messages
    parsed_data = HL7Parser.hl7_to_dataframe(hl7_messages)
    print("\nParsed HL7 data:")
    print(parsed_data)
    
    # De-identify parsed data
    deidentified = HealthcareTransformation.remove_phi(parsed_data)
    print("\nDe-identified HL7 data:")
    print(deidentified)


def example_6_compliance_validation():
    """Example 6: Validate HIPAA compliance."""
    print("\n" + "="*60)
    print("EXAMPLE 6: HIPAA Compliance Validation")
    print("="*60)
    
    # Non-compliant data
    non_compliant = pd.DataFrame({
        'patient_name': ['John Doe', 'Jane Smith'],
        'ssn': ['123-45-6789', '987-65-4321'],
        'age': [43, 95],  # Age >89 should be grouped
        'diagnosis': ['Diabetes', 'Hypertension']
    })
    
    print("\nValidating non-compliant data:")
    report1 = HealthcareTransformation.validate_hipaa_compliance(non_compliant)
    print(f"  Compliant: {report1['compliant']}")
    print(f"  Issues: {report1['issues']}")
    print(f"  Warnings: {report1['warnings']}")
    
    # Compliant data
    compliant = pd.DataFrame({
        'anonymous_id': ['A1B2C3', 'D4E5F6'],
        'age_range': ['40-49', '90+'],
        'diagnosis': ['Diabetes', 'Hypertension'],
        'state': ['MA', 'NY']
    })
    
    print("\nValidating compliant data:")
    report2 = HealthcareTransformation.validate_hipaa_compliance(compliant)
    print(f"  Compliant: {report2['compliant']}")
    print(f"  Issues: {report2['issues']}")
    print(f"  Warnings: {report2['warnings']}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("HEALTHCARE DATA PIPELINE EXAMPLES")
    print("HIPAA-Compliant Data Transformations")
    print("="*60)
    
    example_1_basic_deidentification()
    example_2_safe_harbor_method()
    example_3_pipeline_with_audit()
    example_4_patient_deduplication()
    example_5_hl7_parsing()
    example_6_compliance_validation()
    
    print("\n" + "="*60)
    print("ALL EXAMPLES COMPLETED")
    print("="*60)
    print("\nGenerated files:")
    print("  - deidentified_patients.csv")
    print("  - audit_trail.csv")
    print("\nNext steps:")
    print("  1. Review the de-identified data")
    print("  2. Check the audit trail")
    print("  3. Integrate with your healthcare system")
