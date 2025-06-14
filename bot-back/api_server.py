from flask import Flask, request, jsonify
import uuid
from datetime import datetime
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Mock database
applications_db = []

@app.route('/api/phone-number', methods=['POST'])
def handle_phone_number():
    """Mock API endpoint for handling phone numbers."""
    data = request.get_json()
    phone_number = data.get("phone_number")

    if not phone_number:
        return jsonify({'error': 'Phone number is required'}), 400

    # Simulate saving the phone number
    app.logger.info(f"Received phone number: {phone_number}")
    # peform automation of phone number filling

    return jsonify({'success': True}), 200

# get phone number by number
@app.route('/api/phone-number/<number>', methods=['GET'])
def get_phone_number(number):
    """Get phone number details by number."""
    # Simulate fetching phone number details
    app.logger.info(f"Fetching details for phone number: {number}")
    return jsonify({
        'phone_number': number,
    }), 200

# post for mpin
@app.route('/api/mpin', methods=['POST'])
def submit_mpin():
    """Mock API endpoint for MPIN submissions."""
    data = request.get_json()
    app.logger.info(f"Received MPIN: {data.get('mpin')}")
    return jsonify({'success': True}), 200

# get mpin by number
@app.route('/api/mpin/<number>', methods=['GET'])
def get_mpin(number):
    """Get MPIN details by number."""
    app.logger.info(f"Fetching MPIN for number: {number}")
    return jsonify({
        'number': number,
        'mpin': '1234'
    }), 200

@app.route('/api/driving-license', methods=['POST'])
def submit_driving_license():
    """Mock API endpoint for driving license applications."""
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = [
            'firstname', 'lastname', 'dob', 'citizenshipno', 
            'addresstype', 'issuedistrict', 'issuedistrict_code', 
            'issuedate', 'email'
        ]
        
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Generate application ID
        application_id = f"DL-{str(uuid.uuid4())[:8].upper()}"
        
        # Create application record
        application = {
            'application_id': application_id,
            'submitted_at': datetime.now().isoformat(),
            'status': 'submitted',
            'data': data
        }
        
        # Store in mock database
        applications_db.append(application)
        
        # Log the submission
        app.logger.info(f"New application submitted: {application_id}")
        app.logger.info(f"Applicant: {data.get('firstname')} {data.get('lastname')}")
        
        # Return success response
        return jsonify({
            'success': True,
            'application_id': application_id,
            'message': 'Driving license application submitted successfully',
            'status': 'submitted',
            'estimated_processing_days': 7
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error processing application: {str(e)}")
        return jsonify({
            'error': 'Internal server error'
        }), 500

@app.route('/api/driving-license/<application_id>', methods=['GET'])
# get user submitted data by application ID
def get_applicant_data(application_id):
    """Get application details by application ID."""
    for app_record in applications_db:
        if app_record['application_id'] == application_id:
            return jsonify({
                'application_id': app_record['application_id'],
                'data': app_record['data']
            }), 200
    
    return jsonify({'error': 'Application not found'}), 404

# @app.route('/api/driving-license/<application_id>', methods=['GET'])
# # get user submitted data by application ID
# def get_applicant_data(application_id):
#     """Get applicant data by application ID."""

#     for app_record in applications_db:
#         if app_record['application_id'] == application_id:
#             return jsonify({
#                 'application_id': application_id,
#                 'data': app_record['data']
#             }), 200

#     return jsonify({'error': 'Application not found'}), 404

@app.route('/api/applications', methods=['GET'])
def list_applications():
    """List all applications (for debugging)."""
    return jsonify({
        'total': len(applications_db),
        'applications': [
            {
                'application_id': app['application_id'],
                'submitted_at': app['submitted_at'],
                'status': app['status'],
                'applicant': f"{app['data'].get('firstname')} {app['data'].get('lastname')}"
            }
            for app in applications_db
        ]
    }), 200

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()}), 200

if __name__ == '__main__':
    print("🚀 Starting Mock API Server...")
    print("📡 API will be available at: http://localhost:5001")
    print("🏥 Health check: http://localhost:5001/health")
    print("📋 Applications list: http://localhost:5001/api/applications")
    app.run(host='0.0.0.0', port=5001, debug=True)
