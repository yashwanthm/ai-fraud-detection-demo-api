import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import pickle

app = Flask(__name__)

# Allow CORS for all domains on all routes
CORS(app)

# Read the environment variable
ENV = os.getenv('FLASK_ENV', 'development')  # Default to 'development' if not set

deployed_model_name = "fraud-detection"  # Ensure this is the same as the model name you gave on OpenShift AI
if ENV == 'development':
    rest_url = "https://fraud-ymaheshw-dev.apps.sandbox-m2.ll9k.p1.openshiftapps.com"  # For local and locations other than the same OpenShift Instance
else:
    rest_url = "http://modelmesh-serving:8008"  # If the API is deployed to the same OpenShift Instance

# Construct the inference URL
infer_url = f"{rest_url}/v2/models/{deployed_model_name}/infer"

# Load the scaler.pkl that contains the pre-trained scikit-learn scaler
with open('artifact/scaler.pkl', 'rb') as handle:
    scaler = pickle.load(handle)

# Handle the request to the model server
def rest_request(data):
    json_data = {
        "inputs": [
            {
                "name": "dense_input",
                "shape": [1, 5],
                "datatype": "FP32",
                "data": data
            }
        ]
    }
    response = requests.post(infer_url, json=json_data)
    response_dict = response.json()
    return response_dict['outputs'][0]['data']

# Endpoint
@app.route('/', methods=['POST'])
def check_fraud():
    data = request.json
    prediction = rest_request(scaler.transform([data]).tolist()[0])  # Place a request to the model server from this service
    threshold = 0.95
    if prediction[0] > threshold:
        message = 'fraud'
    else:
        message = 'not fraud'
    return jsonify({'message': message})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
