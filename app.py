import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)

@app.after_request
def apply_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

# Read the environment variable
ENV = os.getenv('FLASK_ENV', 'production')  # Default to 'development' if not set

deployed_model_name = "fraud" # Ensure that this is same as the model name you gave on OpenShift AI
rest_url = "http://modelmesh-serving:8008" # Model Server endpoint

# Construct the inference URL for our model. Change deployed_moodel_name if you change the name of the model
infer_url = f"{rest_url}/v2/models/{deployed_model_name}/infer"

#Load the scaler.pkl that contained pre-trained scikit-learn scaler used to standardize or normalize input data. This ensures that the data fed into your model during inference is scaled consistently with how it was during training, improving model accuracy and performance
import pickle
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
    prediction = rest_request(scaler.transform([data]).tolist()[0]) # place a request to the model server from this service
    threshhold = 0.95
    if (prediction[0] > threshhold):
        message = 'fraud'
    else:
        message = 'not fraud'
    return jsonify({'message': message})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
