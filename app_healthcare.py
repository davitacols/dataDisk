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
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Theme selection (must be before CSS)
if 'theme' not in st.session_state:
    st.session_state.theme = "Light"

theme = st.session_state.theme

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=League+Spartan:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'League Spartan', sans-serif;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: 300;
        color: #151515;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    
    .main-header strong {
        font-weight: 700;
    }
    
    .subtitle {
        font-size: 1.125rem;
        color: #666;
        margin-bottom: 3rem;
        font-weight: 400;
    }
    
    .stButton>button {
        background-color: #151515;
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 0.875rem;
        font-weight: 600;
        border-radius: 4px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        transition: all 0.2s;
    }
    
    .stButton>button:hover {
        background-color: #000;
        transform: translateY(-1px);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        border-bottom: 1px solid #e5e5e5;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-size: 0.875rem;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        color: #666;
        padding: 1rem 0;
    }
    
    .stTabs [aria-selected="true"] {
        color: #151515;
        border-bottom: 2px solid #151515;
    }
    
    .metric-card {
        background: #f7f7f7;
        padding: 1.5rem;
        border-radius: 4px;
        border: 1px solid #e5e5e5;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #151515;
        margin-bottom: 0.25rem;
    }
    
    .metric-label {
        font-size: 0.75rem;
        color: #999;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    .info-box {
        background: #f7f7f7;
        border-left: 3px solid #151515;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
    }
    
    .success-box {
        background: #f0f9f4;
        border-left: 3px solid #10b981;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #fffbeb;
        border-left: 3px solid #f59e0b;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
    }
    
    .error-box {
        background: #fef2f2;
        border-left: 3px solid #ef4444;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
    }
    
    .stDataFrame {
        border: 1px solid #e5e5e5;
    }
    
    h1, h2, h3 {
        font-weight: 300;
        letter-spacing: -0.5px;
    }
    
    h1 strong, h2 strong, h3 strong {
        font-weight: 700;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: """ + ("#151515" if theme == "Dark" else "#f7f7f7") + """;
        padding: 2rem 1rem;
    }
    
    [data-testid="stSidebar"] * {
        color: """ + ("white" if theme == "Dark" else "#151515") + """ !important;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4 {
        color: white !important;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        font-size: 0.75rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stCheckbox label {
        color: rgba(255, 255, 255, 0.9) !important;
        font-size: 0.875rem;
        font-weight: 400;
    }
    
    [data-testid="stSidebar"] hr {
        border-color: """ + ("rgba(255, 255, 255, 0.1)" if theme == "Dark" else "rgba(0, 0, 0, 0.1)") + """;
        margin: 2rem 0;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: """ + ("rgba(255, 255, 255, 0.8)" if theme == "Dark" else "rgba(0, 0, 0, 0.7)") + """ !important;
        font-size: 0.875rem;
        line-height: 1.6;
    }
    
    [data-testid="stSidebar"] strong {
        color: """ + ("white" if theme == "Dark" else "#151515") + """ !important;
        font-weight: 600;
    }
    
    [data-testid="stSidebar"] [data-baseweb="select"] {
        background-color: """ + ("rgba(255, 255, 255, 0.1)" if theme == "Dark" else "white") + """;
        border: 1px solid """ + ("rgba(255, 255, 255, 0.2)" if theme == "Dark" else "#e5e5e5") + """;
    }
    
    [data-testid="stSidebar"] [data-baseweb="checkbox"] {
        border-color: """ + ("rgba(255, 255, 255, 0.3)" if theme == "Dark" else "rgba(0, 0, 0, 0.3)") + """;
    }
    
    /* Main content theme */
    .main {
        background-color: """ + ("#151515" if theme == "Dark" else "#ffffff") + """;
    }
    
    .main h1, .main h2, .main h3, .main h4, .main h5, .main h6 {
        color: """ + ("#ffffff" if theme == "Dark" else "#151515") + """ !important;
    }
    
    .main .stMarkdown p, .main .stMarkdown li, .main .stMarkdown span, .main .stMarkdown div {
        color: """ + ("#ffffff" if theme == "Dark" else "#151515") + """ !important;
    }
    
    .main label, .main .stSelectbox label, .main .stCheckbox label {
        color: """ + ("#ffffff" if theme == "Dark" else "#151515") + """ !important;
    }
    
    .main .stDataFrame, .main table, .main td, .main th {
        background-color: """ + ("#1e1e1e" if theme == "Dark" else "#ffffff") + """;
        color: """ + ("#ffffff" if theme == "Dark" else "#151515") + """ !important;
    }
    
    [data-testid="stMetricValue"] {
        color: """ + ("#ffffff" if theme == "Dark" else "#151515") + """ !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: """ + ("#999" if theme == "Dark" else "#666") + """ !important;
    }
    
    .main-header {
        color: """ + ("#ffffff" if theme == "Dark" else "#151515") + """ !important;
    }
    
    .subtitle {
        color: """ + ("#999" if theme == "Dark" else "#666") + """ !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: """ + ("#999" if theme == "Dark" else "#666") + """ !important;
    }
    
    .stTabs [aria-selected="true"] {
        color: """ + ("#ffffff" if theme == "Dark" else "#151515") + """ !important;
        border-bottom-color: """ + ("#ffffff" if theme == "Dark" else "#151515") + """ !important;
    }
    
    .info-box, .success-box, .warning-box, .error-box {
        background: """ + ("#1e1e1e" if theme == "Dark" else "#f7f7f7") + """;
        color: """ + ("#ffffff" if theme == "Dark" else "#151515") + """ !important;
    }
    
    .info-box *, .success-box *, .warning-box *, .error-box * {
        color: """ + ("#ffffff" if theme == "Dark" else "#151515") + """ !important;
    }
    
    .main .stAlert {
        background-color: """ + ("#1e1e1e" if theme == "Dark" else "#f7f7f7") + """;
        color: """ + ("#ffffff" if theme == "Dark" else "#151515") + """ !important;
    }
    
    .stButton>button {
        background-color: """ + ("#ffffff" if theme == "Dark" else "#151515") + """;
        color: """ + ("#151515" if theme == "Dark" else "#ffffff") + """ !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">dataDisk <strong>Healthcare</strong></h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle" style="text-align: center;">HIPAA-Compliant Patient Data De-identification Platform</p>', unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("### Configuration")

# Theme toggle
theme_selection = st.sidebar.radio(
    "Theme",
    ["Light", "Dark"],
    index=0 if st.session_state.theme == "Light" else 1,
    horizontal=True
)

if theme_selection != st.session_state.theme:
    st.session_state.theme = theme_selection
    st.rerun()

theme = st.session_state.theme

# De-identification method
method = st.sidebar.selectbox(
    "De-identification Method",
    ["Safe Harbor (Recommended)", "Basic PHI Removal", "Custom Pipeline"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Options")
hash_phi = st.sidebar.checkbox("Hash PHI instead of removing", value=False)
generalize_ages = st.sidebar.checkbox("Generalize ages (>89 grouped)", value=True)
mask_dates = st.sidebar.checkbox("Mask dates (shift randomly)", value=True)
create_audit_log = st.sidebar.checkbox("Generate audit log", value=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### Pricing")
st.sidebar.markdown("""
**Starter**  
$299/month  
10K records/month

**Professional**  
$699/month  
100K records/month

**Enterprise**  
$1,999/month  
Unlimited records
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### Support")
st.sidebar.markdown("""
support@datadisk.io  
[Documentation](#)  
[API Reference](#)
""")

# Main content
tab1, tab2, tab3, tab4 = st.tabs(["Upload & Process", "Compliance Check", "Audit Log", "About"])

with tab1:
    st.markdown("### Upload Patient Data")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Upload CSV or Excel file with patient data",
            type=['csv', 'xlsx', 'xls'],
            help="Upload a file containing patient data that needs to be de-identified"
        )
    
    with col2:
        st.markdown("#### Sample Data")
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
            st.success("Sample data loaded successfully")
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                data = pd.read_csv(uploaded_file)
            else:
                data = pd.read_excel(uploaded_file)
            
            st.session_state['data'] = data
            st.success(f"File uploaded successfully. {len(data)} records loaded.")
            
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
    
    # Display and process data
    if 'data' in st.session_state:
        data = st.session_state['data']
        
        st.markdown("---")
        st.markdown("#### Original Data Preview")
        st.dataframe(data.head(10), use_container_width=True)
        
        st.markdown(f"**Total Records:** {len(data)} | **Columns:** {len(data.columns)}")
        
        # Process button
        if st.button("De-identify Data", type="primary", use_container_width=True):
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
                    
                    st.success("Data de-identified successfully")
                    
                except Exception as e:
                    st.error(f"Error processing data: {str(e)}")
        
        # Display processed data
        if 'processed_data' in st.session_state:
            st.markdown("---")
            st.markdown("#### De-identified Data")
            processed_data = st.session_state['processed_data']
            st.dataframe(processed_data.head(10), use_container_width=True)
            
            # Download buttons
            col1, col2 = st.columns(2)
            
            with col1:
                csv = processed_data.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download CSV",
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
                    label="Download Excel",
                    data=buffer,
                    file_name=f"deidentified_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

with tab2:
    st.markdown("### HIPAA Compliance Validation")
    
    if 'processed_data' in st.session_state:
        processed_data = st.session_state['processed_data']
        
        # Run compliance check
        report = HealthcareTransformation.validate_hipaa_compliance(processed_data)
        
        # Display results
        if report['compliant']:
            st.markdown('<div class="success-box"><h4>HIPAA Compliant</h4><p>No compliance issues detected.</p></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="error-box"><h4>Compliance Issues Found</h4></div>', unsafe_allow_html=True)
            for issue in report['issues']:
                st.error(issue)
        
        if report['warnings']:
            st.markdown('<div class="warning-box"><h4>Warnings</h4></div>', unsafe_allow_html=True)
            for warning in report['warnings']:
                st.warning(warning)
        
        # Detailed report
        st.markdown("---")
        st.markdown("#### Detailed Compliance Report")
        
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
            label="Download Compliance Report",
            data=csv,
            file_name=f"compliance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.info("Please process data first to run compliance validation.")

with tab3:
    st.markdown("### Audit Trail")
    
    if 'audit_log' in st.session_state:
        audit_log = st.session_state['audit_log']
        
        st.dataframe(audit_log, use_container_width=True)
        
        # Download audit log
        csv = audit_log.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Audit Log",
            data=csv,
            file_name=f"audit_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
        
        st.info("Audit logs are required for HIPAA compliance. Keep these records for at least 6 years.")
    else:
        st.info("Please process data with audit logging enabled.")

with tab4:
    st.markdown("### About dataDisk Healthcare")
    
    st.markdown("""
    #### HIPAA-Compliant Data De-identification
    
    dataDisk Healthcare Edition helps healthcare providers, researchers, and health tech companies 
    de-identify patient data quickly and compliantly.
    
    #### Key Features
    - **HIPAA Safe Harbor Method**: Automatically removes all 18 HIPAA identifiers
    - **Audit Logging**: Track all data access and transformations
    - **Compliance Validation**: Verify data meets HIPAA requirements
    - **Multiple Formats**: Support for CSV, Excel, and HL7 messages
    - **Fast Processing**: De-identify 10,000 records in under 5 minutes
    
    #### Security & Compliance
    - All processing happens locally (no data sent to cloud)
    - Audit trails for all operations
    - HIPAA Safe Harbor compliant by default
    - Business Associate Agreement (BAA) available
    
    #### Pricing
    
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
    
    #### Contact
    - Email: support@datadisk.io
    - Website: www.datadisk.io
    - Documentation: docs.datadisk.io
    
    #### Legal
    This tool is provided as-is. Users are responsible for ensuring compliance with HIPAA 
    and other applicable regulations. Consult with legal counsel before using in production.
    """)
    
    st.markdown("---")
    st.markdown("dataDisk Healthcare Platform | Version 1.0.0")

# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #999; font-size: 0.875rem; padding: 2rem 0;">All data processing happens locally. No data is sent to external servers.</p>',
    unsafe_allow_html=True
)
