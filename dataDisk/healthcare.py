"""
Healthcare-specific data transformations for HIPAA compliance.
"""

import pandas as pd
import numpy as np
import hashlib
import re
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta


class HealthcareTransformation:
    """HIPAA-compliant healthcare data transformations."""
    
    # HIPAA identifiers that must be removed/masked
    PHI_PATTERNS = {
        'ssn': r'\b\d{3}-?\d{2}-?\d{4}\b',
        'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'zip': r'\b\d{5}(?:-\d{4})?\b',
        'mrn': r'\b[A-Z]{2,3}\d{6,10}\b',  # Medical Record Number
        'ip_address': r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
    }
    
    @staticmethod
    def apply_custom_rules(data: pd.DataFrame, rules: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Apply custom de-identification rules defined by user.
        
        Args:
            data: DataFrame to process
            rules: List of rule dictionaries with format:
                   [{'column': 'col_name', 'pattern': 'regex', 'action': 'redact|hash|remove'}]
        
        Returns:
            Processed DataFrame
        """
        data = data.copy()
        
        for rule in rules:
            column = rule.get('column')
            pattern = rule.get('pattern')
            action = rule.get('action', 'redact')
            
            if column not in data.columns:
                logging.warning(f"Column {column} not found, skipping rule")
                continue
            
            if action == 'remove':
                data = data.drop(column, axis=1)
            
            elif action == 'redact':
                if pattern:
                    data[column] = data[column].astype(str).str.replace(
                        pattern, '[REDACTED]', regex=True
                    )
                else:
                    data[column] = '[REDACTED]'
            
            elif action == 'hash':
                data[column] = data[column].apply(
                    lambda x: hashlib.sha256(str(x).encode()).hexdigest()[:16]
                    if pd.notna(x) else None
                )
            
            elif action == 'mask':
                # Mask all but last 4 characters
                data[column] = data[column].astype(str).apply(
                    lambda x: '*' * (len(x) - 4) + x[-4:] if len(x) > 4 else '****'
                )
        
        logging.info(f"Applied {len(rules)} custom de-identification rules")
        return data
    
    @staticmethod
    def calculate_reidentification_risk(data: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate re-identification risk score using k-anonymity metrics.
        
        Args:
            data: De-identified DataFrame
        
        Returns:
            Dictionary with risk metrics
        """
        risk_report = {
            'overall_risk': 'LOW',
            'k_anonymity': None,
            'unique_combinations': 0,
            'quasi_identifiers': [],
            'recommendations': []
        }
        
        # Identify quasi-identifiers (columns that could be used for re-identification)
        quasi_identifiers = []
        for col in data.columns:
            # Check if column has moderate cardinality (not too unique, not too generic)
            if data[col].dtype in ['object', 'int64', 'float64']:
                unique_ratio = data[col].nunique() / len(data)
                if 0.01 < unique_ratio < 0.9:  # Between 1% and 90% unique
                    quasi_identifiers.append(col)
        
        risk_report['quasi_identifiers'] = quasi_identifiers
        
        if quasi_identifiers:
            # Calculate k-anonymity: minimum group size for quasi-identifier combinations
            group_sizes = data.groupby(quasi_identifiers[:3]).size()  # Use top 3 QIs
            k_anonymity = group_sizes.min() if len(group_sizes) > 0 else len(data)
            risk_report['k_anonymity'] = int(k_anonymity)
            
            # Count unique combinations
            risk_report['unique_combinations'] = len(group_sizes)
            
            # Assess risk level
            if k_anonymity < 5:
                risk_report['overall_risk'] = 'HIGH'
                risk_report['recommendations'].append(
                    'K-anonymity < 5: Consider further generalization or suppression'
                )
            elif k_anonymity < 10:
                risk_report['overall_risk'] = 'MEDIUM'
                risk_report['recommendations'].append(
                    'K-anonymity < 10: Acceptable but could be improved'
                )
            else:
                risk_report['overall_risk'] = 'LOW'
                risk_report['recommendations'].append(
                    f'K-anonymity = {k_anonymity}: Good privacy protection'
                )
        else:
            risk_report['overall_risk'] = 'LOW'
            risk_report['recommendations'].append('No quasi-identifiers detected')
        
        # Check for remaining PHI patterns
        phi_found = []
        for col in data.columns:
            if data[col].dtype == 'object':
                sample = data[col].dropna().astype(str).head(100)
                for phi_type, pattern in HealthcareTransformation.PHI_PATTERNS.items():
                    if sample.str.contains(pattern, regex=True).any():
                        phi_found.append(f"{phi_type} in {col}")
        
        if phi_found:
            risk_report['overall_risk'] = 'HIGH'
            risk_report['recommendations'].append(
                f'PHI patterns detected: {phi_found}'
            )
        
        logging.info(f"Re-identification risk: {risk_report['overall_risk']}")
        return risk_report
    
    @staticmethod
    def remove_phi(data: pd.DataFrame, 
                   columns: Optional[List[str]] = None,
                   hash_instead: bool = False) -> pd.DataFrame:
        """
        Remove Protected Health Information (PHI) from dataset.
        
        Args:
            data: DataFrame containing PHI
            columns: Specific columns to process, or None for all
            hash_instead: If True, hash PHI instead of removing
            
        Returns:
            De-identified DataFrame
        """
        data = data.copy()
        
        # PHI columns to remove/mask
        phi_columns = [
            'first_name', 'last_name', 'name', 'patient_name',
            'ssn', 'social_security', 'phone', 'phone_number',
            'email', 'address', 'street', 'city', 'state', 'zip',
            'mrn', 'medical_record_number', 'account_number',
            'license_number', 'vehicle_id', 'device_id',
            'ip_address', 'url', 'photo', 'biometric'
        ]
        
        target_cols = columns or [col for col in data.columns 
                                  if any(phi in col.lower() for phi in phi_columns)]
        
        for col in target_cols:
            if col in data.columns:
                if hash_instead:
                    data[col] = data[col].apply(
                        lambda x: hashlib.sha256(str(x).encode()).hexdigest()[:16] 
                        if pd.notna(x) else None
                    )
                else:
                    data[col] = '[REDACTED]'
        
        logging.info(f"Removed PHI from {len(target_cols)} columns")
        return data
    
    @staticmethod
    def mask_dates(data: pd.DataFrame, 
                   date_columns: Optional[List[str]] = None,
                   shift_days: int = None) -> pd.DataFrame:
        """
        Mask dates by shifting them randomly (HIPAA safe harbor method).
        
        Args:
            data: DataFrame with date columns
            date_columns: Columns to mask, or None for auto-detect
            shift_days: Fixed shift, or None for random shift per patient
            
        Returns:
            DataFrame with masked dates
        """
        data = data.copy()
        
        if date_columns is None:
            date_columns = data.select_dtypes(include=['datetime64']).columns.tolist()
            date_columns += [col for col in data.columns if 'date' in col.lower()]
        
        for col in date_columns:
            if col in data.columns:
                try:
                    data[col] = pd.to_datetime(data[col], errors='coerce')
                    
                    if shift_days is None:
                        # Random shift between -365 and +365 days
                        shift = np.random.randint(-365, 365)
                    else:
                        shift = shift_days
                    
                    data[col] = data[col] + timedelta(days=shift)
                    
                except Exception as e:
                    logging.warning(f"Could not mask dates in column {col}: {e}")
        
        logging.info(f"Masked dates in {len(date_columns)} columns")
        return data
    
    @staticmethod
    def generalize_ages(data: pd.DataFrame, 
                       age_column: str = 'age',
                       bins: List[int] = None) -> pd.DataFrame:
        """
        Generalize ages into ranges (HIPAA requires ages >89 to be grouped).
        
        Args:
            data: DataFrame with age column
            age_column: Name of age column
            bins: Custom age bins, or None for HIPAA-compliant defaults
            
        Returns:
            DataFrame with generalized ages
        """
        data = data.copy()
        
        if age_column not in data.columns:
            return data
        
        if bins is None:
            bins = [0, 18, 30, 40, 50, 60, 70, 80, 90, 150]
        
        labels = [f"{bins[i]}-{bins[i+1]-1}" for i in range(len(bins)-2)]
        labels.append(f"{bins[-2]}+")  # HIPAA: 90+ grouped
        
        data[f'{age_column}_range'] = pd.cut(
            data[age_column], 
            bins=bins, 
            labels=labels, 
            right=False
        )
        
        logging.info(f"Generalized ages into {len(labels)} ranges")
        return data
    
    @staticmethod
    def create_patient_id(data: pd.DataFrame,
                         source_columns: List[str],
                         id_column: str = 'patient_id') -> pd.DataFrame:
        """
        Create anonymized patient ID from PHI using hashing.
        
        Args:
            data: DataFrame with patient data
            source_columns: Columns to use for ID generation
            id_column: Name for new ID column
            
        Returns:
            DataFrame with anonymized patient IDs
        """
        data = data.copy()
        
        def generate_id(row):
            combined = ''.join(str(row[col]) for col in source_columns if col in row.index)
            return hashlib.sha256(combined.encode()).hexdigest()[:12]
        
        data[id_column] = data.apply(generate_id, axis=1)
        
        logging.info(f"Created anonymized patient IDs")
        return data
    
    @staticmethod
    def deduplicate_patients(data: pd.DataFrame,
                           match_columns: List[str] = None,
                           threshold: float = 0.85) -> pd.DataFrame:
        """
        Deduplicate patient records using fuzzy matching.
        
        Args:
            data: DataFrame with patient records
            match_columns: Columns to use for matching
            threshold: Similarity threshold (0-1)
            
        Returns:
            Deduplicated DataFrame
        """
        data = data.copy()
        
        if match_columns is None:
            match_columns = ['first_name', 'last_name', 'dob']
        
        # Simple deduplication based on exact matches
        # In production, use fuzzy matching library like fuzzywuzzy
        available_cols = [col for col in match_columns if col in data.columns]
        
        if available_cols:
            data['_match_key'] = data[available_cols].astype(str).agg('_'.join, axis=1)
            data = data.drop_duplicates(subset=['_match_key'], keep='first')
            data = data.drop('_match_key', axis=1)
            
            logging.info(f"Deduplicated patients using {available_cols}")
        
        return data
    
    @staticmethod
    def validate_hipaa_compliance(data: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate dataset for HIPAA compliance issues.
        
        Args:
            data: DataFrame to validate
            
        Returns:
            Dictionary with compliance report
        """
        report = {
            'compliant': True,
            'issues': [],
            'warnings': [],
            'timestamp': datetime.now().isoformat()
        }
        
        # Check for direct identifiers
        phi_columns = ['ssn', 'social_security', 'name', 'first_name', 'last_name',
                      'phone', 'email', 'address', 'mrn']
        
        found_phi = [col for col in data.columns if any(phi in col.lower() for phi in phi_columns)]
        
        if found_phi:
            report['compliant'] = False
            report['issues'].append(f"Found PHI columns: {found_phi}")
        
        # Check for ages > 89
        age_cols = [col for col in data.columns if 'age' in col.lower()]
        for col in age_cols:
            if col in data.columns and data[col].dtype in ['int64', 'float64']:
                if (data[col] > 89).any():
                    report['warnings'].append(f"Ages >89 found in {col} - should be grouped")
        
        # Check for small cell sizes (< 5 patients in a group)
        if len(data) < 5:
            report['warnings'].append("Dataset has <5 records - may not meet minimum cell size")
        
        # Check for dates
        date_cols = data.select_dtypes(include=['datetime64']).columns.tolist()
        if date_cols:
            report['warnings'].append(f"Date columns found: {date_cols} - ensure dates are shifted")
        
        logging.info(f"HIPAA compliance check: {'PASS' if report['compliant'] else 'FAIL'}")
        return report
    
    @staticmethod
    def generate_audit_log(data: pd.DataFrame,
                          operation: str,
                          user: str = 'system') -> pd.DataFrame:
        """
        Generate audit log entry for data access (HIPAA requirement).
        
        Args:
            data: DataFrame being accessed
            operation: Type of operation (read, write, transform)
            user: User performing operation
            
        Returns:
            Audit log DataFrame
        """
        audit_entry = pd.DataFrame([{
            'timestamp': datetime.now().isoformat(),
            'user': user,
            'operation': operation,
            'record_count': len(data),
            'columns_accessed': ','.join(data.columns.tolist()),
            'data_hash': hashlib.sha256(str(data.values).encode()).hexdigest()[:16]
        }])
        
        logging.info(f"Audit log: {user} performed {operation} on {len(data)} records")
        return audit_entry
    
    @staticmethod
    def safe_harbor_deidentification(data: pd.DataFrame) -> pd.DataFrame:
        """
        Apply HIPAA Safe Harbor de-identification method.
        Removes all 18 HIPAA identifiers.
        
        Args:
            data: DataFrame with PHI
            
        Returns:
            De-identified DataFrame
        """
        data = data.copy()
        
        # Remove direct identifiers by dropping PHI columns entirely
        phi_columns = [
            'first_name', 'last_name', 'name', 'patient_name',
            'ssn', 'social_security', 'phone', 'phone_number',
            'email', 'address', 'street', 'city', 'zip',
            'mrn', 'medical_record_number', 'account_number',
            'license_number', 'vehicle_id', 'device_id',
            'ip_address', 'url', 'biometric'
        ]
        
        cols_to_drop = [col for col in data.columns if any(phi in col.lower() for phi in phi_columns)]
        data = data.drop(columns=cols_to_drop, errors='ignore')
        
        # Generalize ages >89
        if 'age' in data.columns:
            data = HealthcareTransformation.generalize_ages(data)
            # Drop original age column after creating age_range
            if 'age_range' in data.columns:
                data = data.drop('age', axis=1)
        
        # Mask dates
        data = HealthcareTransformation.mask_dates(data)
        
        # Remove geographic subdivisions smaller than state
        geo_cols = ['county', 'city_code', 'postal_code']
        for col in geo_cols:
            if col in data.columns:
                data = data.drop(col, axis=1)
        
        logging.info("Applied HIPAA Safe Harbor de-identification")
        return data
    
    @staticmethod
    def get_risk_summary(risk_report: Dict[str, Any]) -> str:
        """
        Generate human-readable risk summary.
        
        Args:
            risk_report: Risk report from calculate_reidentification_risk()
        
        Returns:
            Formatted risk summary string
        """
        summary = f"""Re-identification Risk Assessment
{'='*50}
Overall Risk Level: {risk_report['overall_risk']}
K-Anonymity Score: {risk_report['k_anonymity']}
Unique Combinations: {risk_report['unique_combinations']}
Quasi-Identifiers: {', '.join(risk_report['quasi_identifiers']) if risk_report['quasi_identifiers'] else 'None'}

Recommendations:
"""
        for i, rec in enumerate(risk_report['recommendations'], 1):
            summary += f"{i}. {rec}\n"
        
        return summary


class HL7Parser:
    """Parse HL7 messages (common healthcare data format)."""
    
    @staticmethod
    def parse_hl7_message(message: str) -> Dict[str, Any]:
        """
        Parse HL7 message into structured data.
        
        Args:
            message: HL7 message string
            
        Returns:
            Dictionary with parsed fields
        """
        segments = message.strip().split('\n')
        parsed = {}
        
        for segment in segments:
            fields = segment.split('|')
            segment_type = fields[0]
            
            if segment_type == 'PID':  # Patient Identification
                parsed['patient_id'] = fields[3] if len(fields) > 3 else None
                parsed['patient_name'] = fields[5] if len(fields) > 5 else None
                parsed['dob'] = fields[7] if len(fields) > 7 else None
                parsed['gender'] = fields[8] if len(fields) > 8 else None
            
            elif segment_type == 'OBX':  # Observation/Result
                parsed['observation'] = fields[3] if len(fields) > 3 else None
                parsed['value'] = fields[5] if len(fields) > 5 else None
                parsed['units'] = fields[6] if len(fields) > 6 else None
        
        return parsed
    
    @staticmethod
    def hl7_to_dataframe(messages: List[str]) -> pd.DataFrame:
        """
        Convert multiple HL7 messages to DataFrame.
        
        Args:
            messages: List of HL7 message strings
            
        Returns:
            DataFrame with parsed HL7 data
        """
        parsed_messages = [HL7Parser.parse_hl7_message(msg) for msg in messages]
        return pd.DataFrame(parsed_messages)
