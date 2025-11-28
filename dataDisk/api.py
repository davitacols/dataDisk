"""
REST API for batch processing healthcare data de-identification.
"""
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import pandas as pd
import os
import uuid
from datetime import datetime
from .healthcare import HealthcareTransformation

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Store job status
jobs = {}


@app.route('/api/v1/deidentify', methods=['POST'])
def deidentify():
    """
    De-identify uploaded CSV/Excel file.
    
    Request:
        - file: CSV or Excel file
        - method: 'safe_harbor', 'phi_removal', or 'custom'
        - custom_rules: JSON array of custom PHI patterns (optional)
    
    Response:
        - job_id: Unique job identifier
        - status: 'processing', 'completed', 'failed'
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400
    
    method = request.form.get('method', 'safe_harbor')
    custom_rules = request.form.get('custom_rules', '[]')
    
    # Generate job ID
    job_id = str(uuid.uuid4())
    
    # Save uploaded file
    filename = secure_filename(file.filename)
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{job_id}_{filename}")
    file.save(input_path)
    
    # Process file
    try:
        # Load data
        if filename.endswith('.csv'):
            data = pd.read_csv(input_path)
        elif filename.endswith(('.xlsx', '.xls')):
            data = pd.read_excel(input_path)
        else:
            return jsonify({'error': 'Unsupported file format'}), 400
        
        # Apply transformation
        transformer = HealthcareTransformation()
        
        if method == 'safe_harbor':
            result = transformer.safe_harbor_deidentification(data)
        elif method == 'phi_removal':
            result = transformer.remove_phi(data)
        elif method == 'custom':
            import json
            rules = json.loads(custom_rules)
            result = transformer.apply_custom_rules(data, rules)
        else:
            return jsonify({'error': 'Invalid method'}), 400
        
        # Calculate risk score
        risk_score = transformer.calculate_reidentification_risk(result)
        
        # Save output
        output_filename = f"deidentified_{filename}"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], f"{job_id}_{output_filename}")
        
        if filename.endswith('.csv'):
            result.to_csv(output_path, index=False)
        else:
            result.to_excel(output_path, index=False)
        
        # Store job info
        jobs[job_id] = {
            'status': 'completed',
            'created_at': datetime.now().isoformat(),
            'input_file': filename,
            'output_file': output_filename,
            'output_path': output_path,
            'records_processed': len(result),
            'method': method,
            'risk_score': risk_score
        }
        
        return jsonify({
            'job_id': job_id,
            'status': 'completed',
            'records_processed': len(result),
            'risk_score': risk_score,
            'download_url': f'/api/v1/download/{job_id}'
        }), 200
        
    except Exception as e:
        jobs[job_id] = {
            'status': 'failed',
            'error': str(e),
            'created_at': datetime.now().isoformat()
        }
        return jsonify({'job_id': job_id, 'status': 'failed', 'error': str(e)}), 500


@app.route('/api/v1/status/<job_id>', methods=['GET'])
def get_status(job_id):
    """Get job status."""
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify(jobs[job_id]), 200


@app.route('/api/v1/download/<job_id>', methods=['GET'])
def download(job_id):
    """Download de-identified file."""
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    job = jobs[job_id]
    if job['status'] != 'completed':
        return jsonify({'error': 'Job not completed'}), 400
    
    return send_file(job['output_path'], as_attachment=True, download_name=job['output_file'])


@app.route('/api/v1/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'version': '1.0.0'}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
