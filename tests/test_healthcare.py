"""
Tests for healthcare transformations.
"""

import pytest
import pandas as pd
import numpy as np
from dataDisk.healthcare import HealthcareTransformation, HL7Parser


class TestHealthcareTransformation:
    
    def test_remove_phi(self):
        """Test PHI removal."""
        data = pd.DataFrame({
            'patient_id': ['P001', 'P002'],
            'first_name': ['John', 'Jane'],
            'last_name': ['Doe', 'Smith'],
            'ssn': ['123-45-6789', '987-65-4321'],
            'diagnosis': ['Diabetes', 'Hypertension']
        })
        
        result = HealthcareTransformation.remove_phi(data)
        
        assert result['first_name'].iloc[0] == '[REDACTED]'
        assert result['last_name'].iloc[0] == '[REDACTED]'
        assert result['ssn'].iloc[0] == '[REDACTED]'
        assert result['diagnosis'].iloc[0] == 'Diabetes'  # Not PHI
    
    def test_remove_phi_with_hashing(self):
        """Test PHI removal with hashing."""
        data = pd.DataFrame({
            'patient_id': ['P001', 'P002'],
            'first_name': ['John', 'Jane']
        })
        
        result = HealthcareTransformation.remove_phi(data, hash_instead=True)
        
        assert result['first_name'].iloc[0] != 'John'
        assert len(result['first_name'].iloc[0]) == 16  # Hash length
    
    def test_generalize_ages(self):
        """Test age generalization."""
        data = pd.DataFrame({
            'patient_id': ['P001', 'P002', 'P003'],
            'age': [25, 45, 95]
        })
        
        result = HealthcareTransformation.generalize_ages(data)
        
        assert 'age_range' in result.columns
        assert result['age_range'].iloc[0] == '18-29'
        assert result['age_range'].iloc[2] == '90+'  # HIPAA requirement
    
    def test_create_patient_id(self):
        """Test anonymous patient ID creation."""
        data = pd.DataFrame({
            'first_name': ['John', 'Jane'],
            'last_name': ['Doe', 'Smith'],
            'dob': ['1980-05-15', '1975-08-22']
        })
        
        result = HealthcareTransformation.create_patient_id(
            data,
            source_columns=['first_name', 'last_name', 'dob']
        )
        
        assert 'patient_id' in result.columns
        assert len(result['patient_id'].iloc[0]) == 12
        assert result['patient_id'].iloc[0] != result['patient_id'].iloc[1]
    
    def test_deduplicate_patients(self):
        """Test patient deduplication."""
        data = pd.DataFrame({
            'first_name': ['John', 'John', 'Jane'],
            'last_name': ['Doe', 'Doe', 'Smith'],
            'dob': ['1980-05-15', '1980-05-15', '1975-08-22']
        })
        
        result = HealthcareTransformation.deduplicate_patients(
            data,
            match_columns=['first_name', 'last_name', 'dob']
        )
        
        assert len(result) == 2  # One duplicate removed
    
    def test_validate_hipaa_compliance_fail(self):
        """Test HIPAA validation with non-compliant data."""
        data = pd.DataFrame({
            'patient_name': ['John Doe'],
            'ssn': ['123-45-6789']
        })
        
        report = HealthcareTransformation.validate_hipaa_compliance(data)
        
        assert report['compliant'] == False
        assert len(report['issues']) > 0
    
    def test_validate_hipaa_compliance_pass(self):
        """Test HIPAA validation with compliant data."""
        data = pd.DataFrame({
            'anonymous_id': ['A1B2C3'],
            'diagnosis': ['Diabetes'],
            'state': ['MA']
        })
        
        report = HealthcareTransformation.validate_hipaa_compliance(data)
        
        assert report['compliant'] == True
    
    def test_generate_audit_log(self):
        """Test audit log generation."""
        data = pd.DataFrame({
            'patient_id': ['P001', 'P002'],
            'diagnosis': ['Diabetes', 'Hypertension']
        })
        
        audit = HealthcareTransformation.generate_audit_log(
            data,
            operation='read',
            user='test_user'
        )
        
        assert len(audit) == 1
        assert audit['user'].iloc[0] == 'test_user'
        assert audit['operation'].iloc[0] == 'read'
        assert audit['record_count'].iloc[0] == 2
    
    def test_safe_harbor_deidentification(self):
        """Test Safe Harbor de-identification."""
        data = pd.DataFrame({
            'first_name': ['John'],
            'last_name': ['Doe'],
            'ssn': ['123-45-6789'],
            'age': [95],
            'city': ['Boston'],
            'diagnosis': ['Diabetes']
        })
        
        result = HealthcareTransformation.safe_harbor_deidentification(data)
        
        assert 'first_name' not in result.columns or result['first_name'].iloc[0] == '[REDACTED]'
        assert 'city' not in result.columns  # Geographic data removed
        assert 'diagnosis' in result.columns  # Clinical data preserved


class TestHL7Parser:
    
    def test_parse_hl7_message(self):
        """Test HL7 message parsing."""
        message = """MSH|^~\\&|LAB|Hospital|EMR|Clinic|20240115120000||ORU^R01|MSG001|P|2.5
PID|1||P001||Doe^John||19800515|M|||123 Main St^^Boston^MA^02101
OBX|1|NM|GLU^Glucose||95|mg/dL|70-100|N|||F"""
        
        result = HL7Parser.parse_hl7_message(message)
        
        assert result['patient_id'] == 'P001'
        assert result['patient_name'] == 'Doe^John'
        assert result['dob'] == '19800515'
        assert result['gender'] == 'M'
    
    def test_hl7_to_dataframe(self):
        """Test converting multiple HL7 messages to DataFrame."""
        messages = [
            """MSH|^~\\&|LAB|Hospital|EMR|Clinic|20240115120000||ORU^R01|MSG001|P|2.5
PID|1||P001||Doe^John||19800515|M|||123 Main St^^Boston^MA^02101""",
            """MSH|^~\\&|LAB|Hospital|EMR|Clinic|20240116130000||ORU^R01|MSG002|P|2.5
PID|1||P002||Smith^Jane||19750822|F|||456 Oak Ave^^New York^NY^10001"""
        ]
        
        result = HL7Parser.hl7_to_dataframe(messages)
        
        assert len(result) == 2
        assert result['patient_id'].iloc[0] == 'P001'
        assert result['patient_id'].iloc[1] == 'P002'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
