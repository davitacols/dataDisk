"""
Healthcare Data De-identification Web App
Simple Streamlit interface for HIPAA-compliant data processing
"""

import streamlit as st
import pandas as pd
import io
from datetime import datetime
from dataDisk.healthcare import HealthcareTransformation, HL7Parser
from dataDisk.pipeline import DataPipeline

# Page config
st.set_page_config(
    page_title="dataDisk Healthcare - HIPAA De-identification",
    page_icon="🏥",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .warning-box {
        padding: 1rem;
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🏥 dataDisk Healthcare Edition</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem;">HIPAA-Compliant Patient Data De-identification</p>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("⚙️ Settings")
st.sidebar.markdown("---")

# De-identification method
method = st.sidebar.selectbox(
    "De-identification Method",
    ["Safe Harbor (Recommended)", "Basic PHI Removal", "Custom Pipeline"]
)

# Additional options
st.sidebar.markdown("### Options")
hash_phi = st.sidebar.checkbox("Hash PHI instead of removing", value=False)
generalize_ages = st.sidebar.checkbox("Generalize ages (>89 grouped)", value=True)
mask_dates = st.sidebar.checkbox("Mask dates (shift randomly)", value=True)
create_audit_log = st.sidebar.checkbox("Generate audit log", value=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Pricing")
st.sidebar.info("**Starter**: $299/month\n- Up to 10K records/month\n- Basic de-identification\n- Email support")
st.sidebar.success("**Professional**: $699/month\n- Up to 100K records/month\n- Advanced features\n- API access")

# Main content
tab1, tab2, tab3, tab4 = st.tabs(["📤 Upload & Process", "📋 Compliance Check", "📊 Audit Log", "ℹ️ About"])

with tab1:
    st.header("Upload Patient Data")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Upload CSV or Excel file with patient data",
            type=['csv', 'xlsx', 'xls'],
            help="Upload a file containing patient data that needs to be de-identified"
        )
    
    with col2:
        st.markdown("### Sample Data")
        if st.button("Load Sample Dataset"):
            sample_data = pd.DataFrame({
                'patient_id': ['P001', 'P002', 'P003'],
                'first_name': ['John', 'Jane', 'Bob'],
                'last_name': ['Doe', 'Smith', 'Johnson'],
                'ssn': ['123-45-6789', '987-65-4321', '555-12-3456'],
                'age': [43, 48, 95],
                'diagnosis': ['Diabetes', 'Hypertension', 'Asthma']
            })
            st.session_state['data'] = sample_data
            st.success("Sample data loaded!")
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                data = pd.read_csv(uploaded_file)
            else:
                data = pd.read_excel(uploaded_file)
            
            st.session_state['data'] = data
            st.success(f"✅ File uploaded successfully! {len(data)} records loaded.")
            
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
    
    # Display and process data
    if 'data' in st.session_state:
        data = st.session_state['data']
        
        st.markdown("---")
        st.subheader("Original Data Preview")
        st.dataframe(data.head(10), use_container_width=True)
        
        st.markdown(f"**Total Records:** {len(data)} | **Columns:** {len(data.columns)}")
        
        # Process button
        if st.button("🔒 De-identify Data", type="primary", use_container_width=True):
            with st.spinner("Processing data..."):
                try:
                    # Apply de-identification based on method
                    if method == "Safe Harbor (Recommended)":
                        processed_data = HealthcareTransformation.safe_harbor_deidentification(data)
                    
                    elif method == "Basic PHI Removal":
                        processed_data = HealthcareTransformation.remove_phi(data, hash_instead=hash_phi)
                        if generalize_ages and 'age' in processed_data.columns:
                            processed_data = HealthcareTransformation.generalize_ages(processed_data)
                        if mask_dates:
                            processed_data = HealthcareTransformation.mask_dates(processed_data)
                    
                    else:  # Custom Pipeline
                        pipeline = DataPipeline()
                        pipeline.add_step(lambda df: HealthcareTransformation.create_patient_id(
                            df, source_columns=['first_name', 'last_name'] if 'first_name' in df.columns else df.columns[:2].tolist()
                        ))
                        pipeline.add_step(lambda df: HealthcareTransformation.remove_phi(df, hash_instead=hash_phi))
                        if generalize_ages:
                            pipeline.add_step(lambda df: HealthcareTransformation.generalize_ages(df) if 'age' in df.columns else df)
                        if mask_dates:
                            pipeline.add_step(lambda df: HealthcareTransformation.mask_dates(df))
                        processed_data = pipeline.run(data)
                    
                    st.session_state['processed_data'] = processed_data
                    
                    # Generate audit log
                    if create_audit_log:
                        audit_log = HealthcareTransformation.generate_audit_log(
                            processed_data,
                            operation='de-identification',
                            user='web_user'
                        )
                        st.session_state['audit_log'] = audit_log
                    
                    st.success("✅ Data de-identified successfully!")
                    
                except Exception as e:
                    st.error(f"❌ Error processing data: {str(e)}")
        
        # Display processed data
        if 'processed_data' in st.session_state:
            st.markdown("---")
            st.subheader("De-identified Data")
            processed_data = st.session_state['processed_data']
            st.dataframe(processed_data.head(10), use_container_width=True)
            
            # Download buttons
            col1, col2 = st.columns(2)
            
            with col1:
                csv = processed_data.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv,
                    file_name=f"deidentified_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col2:
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    processed_data.to_excel(writer, index=False, sheet_name='De-identified')
                buffer.seek(0)
                
                st.download_button(
                    label="📥 Download as Excel",
                    data=buffer,
                    file_name=f"deidentified_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

with tab2:
    st.header("HIPAA Compliance Validation")
    
    if 'processed_data' in st.session_state:
        processed_data = st.session_state['processed_data']
        
        # Run compliance check
        report = HealthcareTransformation.validate_hipaa_compliance(processed_data)
        
        # Display results
        if report['compliant']:
            st.markdown('<div class="success-box"><h3>✅ HIPAA Compliant</h3><p>No compliance issues detected.</p></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="error-box"><h3>❌ Compliance Issues Found</h3></div>', unsafe_allow_html=True)
            for issue in report['issues']:
                st.error(f"🚨 {issue}")
        
        if report['warnings']:
            st.markdown('<div class="warning-box"><h3>⚠️ Warnings</h3></div>', unsafe_allow_html=True)
            for warning in report['warnings']:
                st.warning(f"⚠️ {warning}")
        
        # Detailed report
        st.markdown("---")
        st.subheader("Detailed Compliance Report")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Compliance Status", "PASS" if report['compliant'] else "FAIL")
        with col2:
            st.metric("Issues Found", len(report['issues']))
        with col3:
            st.metric("Warnings", len(report['warnings']))
        
        # Download report
        report_df = pd.DataFrame([report])
        csv = report_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Compliance Report",
            data=csv,
            file_name=f"compliance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.info("👆 Please process data first to run compliance validation.")

with tab3:
    st.header("Audit Trail")
    
    if 'audit_log' in st.session_state:
        audit_log = st.session_state['audit_log']
        
        st.dataframe(audit_log, use_container_width=True)
        
        # Download audit log
        csv = audit_log.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Audit Log",
            data=csv,
            file_name=f"audit_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
        
        st.info("💡 Audit logs are required for HIPAA compliance. Keep these records for at least 6 years.")
    else:
        st.info("👆 Please process data with audit logging enabled.")

with tab4:
    st.header("About dataDisk Healthcare Edition")
    
    st.markdown("""
    ### 🏥 HIPAA-Compliant Data De-identification
    
    dataDisk Healthcare Edition helps healthcare providers, researchers, and health tech companies 
    de-identify patient data quickly and compliantly.
    
    #### ✨ Key Features
    - **HIPAA Safe Harbor Method**: Automatically removes all 18 HIPAA identifiers
    - **Audit Logging**: Track all data access and transformations
    - **Compliance Validation**: Verify data meets HIPAA requirements
    - **Multiple Formats**: Support for CSV, Excel, and HL7 messages
    - **Fast Processing**: De-identify 10,000 records in under 5 minutes
    
    #### 🔒 Security & Compliance
    - All processing happens locally (no data sent to cloud)
    - Audit trails for all operations
    - HIPAA Safe Harbor compliant by default
    - Business Associate Agreement (BAA) available
    
    #### 💰 Pricing
    
    **Starter - $299/month**
    - Up to 10,000 records/month
    - Basic de-identification
    - CSV/Excel support
    - Email support
    
    **Professional - $699/month**
    - Up to 100,000 records/month
    - Advanced features (HL7, API)
    - Database connectors
    - Priority support
    
    **Enterprise - $1,999/month**
    - Unlimited records
    - Custom integrations
    - On-premise deployment
    - Dedicated support
    - BAA included
    
    #### 📞 Contact
    - Email: support@datadisk.io
    - Website: www.datadisk.io
    - Documentation: docs.datadisk.io
    
    #### 📄 Legal
    This tool is provided as-is. Users are responsible for ensuring compliance with HIPAA 
    and other applicable regulations. Consult with legal counsel before using in production.
    """)
    
    st.markdown("---")
    st.markdown("Made with ❤️ by dataDisk | Version 1.0.0")

# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #666;">🔒 All data processing happens locally. No data is sent to external servers.</p>',
    unsafe_allow_html=True
)
