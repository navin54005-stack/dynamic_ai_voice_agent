# app.py
from flask import Flask, request, render_template, jsonify, session
from dynamic_ai_model import DynamicVoiceAgent
from utils.csv_processor import CSVProcessor
import os
import secrets
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Auto-generate secret key if not set in environment
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', secrets.token_hex(16))
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize AI agent
dynamic_agent = DynamicVoiceAgent()

@app.route('/')
def index():
    """Serve the main HTML interface"""
    return render_template('index.html')

@app.route('/upload-company-data', methods=['POST'])
def upload_company_data():
    """Upload and process company CSV data with smart detection"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file selected'})
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
        
        # Check file extension
        if not file.filename.endswith('.csv'):
            return jsonify({'success': False, 'error': 'Please upload a CSV file'})
        
        # Process CSV with smart detection
        records, columns, is_valid, column_mapping = CSVProcessor.process_uploaded_csv(file)
        
        if not is_valid:
            return jsonify({'success': False, 'error': 'Could not find recognizable company or contact information columns'})
        
        # Load into dynamic agent with column mapping
        dynamic_agent.load_company_data(records, columns, column_mapping)
        
        # Store in session
        session['company_data'] = {
            'records': records,
            'columns': columns,
            'column_mapping': column_mapping,
            'upload_time': datetime.now().isoformat()
        }
        
        # Get company info for confirmation
        company_info = CSVProcessor.extract_smart_company_info(records, column_mapping)
        
        return jsonify({
            'success': True,
            'message': f'Successfully loaded company data for {company_info["name"]}',
            'company_info': company_info,
            'columns': columns,
            'record_count': len(records)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'Upload error: {str(e)}'})

@app.route('/get-ai-response', methods=['POST'])
def get_ai_response():
    """Get AI response to customer input"""
    try:
        data = request.json
        customer_response = data.get('customer_response', '')
        customer_data = data.get('customer_data', {})
        
        # Check if company data is loaded
        if not session.get('company_data'):
            return jsonify({
                'success': False, 
                'error': 'Please upload company data first'
            })
        
        # Generate short response (5-10 seconds speaking)
        ai_response = dynamic_agent.generate_short_response(customer_response, customer_data)
        
        return jsonify({
            'success': True,
            'ai_response': ai_response
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/get-learning-insights')
def get_learning_insights():
    """Get AI learning insights"""
    try:
        insights = dynamic_agent.get_learning_insights()
        return jsonify({'success': True, 'insights': insights})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'company_data_loaded': session.get('company_data') is not None
    })

@app.route('/clear-session', methods=['POST'])
def clear_session():
    """Clear session data"""
    try:
        session.clear()
        return jsonify({'success': True, 'message': 'Session cleared successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 DYNAMIC VOICE AGENT SERVER STARTING...")
    print("=" * 50)
    print(f"🔑 Secret Key: {app.config['SECRET_KEY'][:8]}...")
    print("📁 Visit: http://127.0.0.1:5000")
    print("🧪 Test: http://127.0.0.1:5000/health")
    print("🗑️  Clear: http://127.0.0.1:5000/clear-session")
    print("=" * 50)
    
    # Create necessary directories
    os.makedirs('data/patterns', exist_ok=True)
    os.makedirs('uploads', exist_ok=True)
    
    app.run(debug=True, host='127.0.0.1', port=5000)

