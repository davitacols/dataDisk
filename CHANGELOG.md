# Changelog

All notable changes to dataDisk Healthcare will be documented in this file.

## [1.1.0] - 2024-01-15

### Added
- **Batch Processing API**: REST API for automated de-identification
  - POST /api/v1/deidentify - Upload and process files
  - GET /api/v1/status/{job_id} - Check job status
  - GET /api/v1/download/{job_id} - Download results
  - GET /api/v1/health - Health check endpoint
  
- **Custom Rules Engine**: Flexible de-identification rules
  - Support for redact, mask, hash, and remove actions
  - Regex pattern matching for custom PHI detection
  - Reusable rule sets for consistent processing
  - API integration for programmatic rule application

- **Re-identification Risk Scoring**: K-anonymity analysis
  - Automatic quasi-identifier detection
  - K-anonymity calculation
  - Risk level assessment (LOW/MEDIUM/HIGH)
  - PHI pattern detection in de-identified data
  - Detailed recommendations for improvement
  - Risk summary reports

- **Web Interface Enhancements**:
  - Risk score display after de-identification
  - Expandable risk details with recommendations
  - Visual risk level indicators
  - K-anonymity metrics

### Changed
- Updated Streamlit app to show risk scores automatically
- Enhanced compliance validation with risk metrics
- Improved audit logging with risk assessment data

### Documentation
- Added NEW_FEATURES.md with comprehensive feature documentation
- Created API_QUICKSTART.md for rapid API onboarding
- Added 3 new example files:
  - custom_rules_example.py
  - api_example.py
  - risk_score_example.py

### Dependencies
- Added Flask >= 2.3.0 for API server
- Added requests >= 2.31.0 for API client examples

## [1.0.0] - 2024-01-10

### Added
- Initial release of dataDisk Healthcare
- HIPAA Safe Harbor de-identification
- Basic PHI removal
- Age generalization (>89 grouped)
- Date masking with random shifts
- Audit logging
- HL7 message parsing
- Patient deduplication
- HIPAA compliance validation
- Streamlit web interface
- Professional Getty Images-inspired design
- Mock data generator (1000 records)
- Comprehensive test suite
- Healthcare examples
- Business documentation

### Features
- CSV and Excel file support
- Multiple de-identification methods
- Compliance checking
- Audit trail generation
- Download results in CSV/Excel formats

### Documentation
- README.md with quick start guide
- HEALTHCARE_MVP.md with go-to-market strategy
- DEPLOYMENT_GUIDE.md for production setup
- Landing page for GitHub Pages

## [0.1.0] - 2024-01-05

### Added
- Core dataDisk package
- DataPipeline framework
- Transformation classes
- Validator classes
- ParallelProcessor
- Data sources (CSV)
- Data sinks (CSV, Excel, SQLite)
- Basic transformations (normalize, standardize)
- Label encoding
- One-hot encoding

---

## Upcoming Features

### [1.2.0] - Planned Q1 2024
- Multi-file batch processing in web interface
- Scheduled jobs (recurring de-identification)
- Team collaboration features
- Enhanced audit dashboard
- Data quality checks

### [1.3.0] - Planned Q2 2024
- Database connectors (MySQL, PostgreSQL, SQL Server)
- EHR integration (Epic, Cerner, Allscripts)
- Custom de-identification profiles
- Synthetic data generation
- GDPR compliance mode

### [2.0.0] - Planned Q3 2024
- AI-powered PHI detection
- Differential privacy
- Blockchain audit trail
- Mobile app (iOS/Android)
- White-label solution

---

## Version History

| Version | Release Date | Key Features |
|---------|--------------|--------------|
| 1.1.0 | 2024-01-15 | API, Custom Rules, Risk Scoring |
| 1.0.0 | 2024-01-10 | Initial Healthcare Release |
| 0.1.0 | 2024-01-05 | Core Package |

---

## Migration Guide

### Upgrading from 1.0.0 to 1.1.0

No breaking changes. All existing code continues to work.

**New features are opt-in:**

```python
# Old code still works
result = HealthcareTransformation.safe_harbor_deidentification(data)

# New: Add risk scoring
risk = HealthcareTransformation.calculate_reidentification_risk(result)

# New: Use custom rules
rules = [{'column': 'ssn', 'action': 'redact'}]
result = HealthcareTransformation.apply_custom_rules(data, rules)

# New: Use API
# python -m dataDisk.api
```

**Install new dependencies:**

```bash
pip install --upgrade dataDisk
# or
pip install flask requests
```

---

## Support

For questions about changes or upgrade assistance:
- Email: support@datadisk.io
- Documentation: docs.datadisk.io
- GitHub Issues: github.com/davitacols/dataDisk/issues
