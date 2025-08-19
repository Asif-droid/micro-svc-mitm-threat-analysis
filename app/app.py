from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Flask on Minikube via Istio!"

@app.route("/app2")
def app2():
    try:
        res = requests.get("http://flask-app-2:5001/compute")  # internal service call
        # res = requests.get("http://localhost:5001/compute")  # internal service call
        data = res.json()
        return jsonify({"message": "Got result from app 2", "data": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
