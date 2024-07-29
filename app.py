from flask import Flask, jsonify
import requests

app = Flask(__name__)


deployed_model_name = "fraud-detection"
# rest_url = "http://modelmesh-serving:8008"
rest_url = "https://fraud-detection-ymaheshw-dev.apps.sandbox-m2.ll9k.p1.openshiftapps.com"

infer_url = f"{rest_url}/v2/models/{deployed_model_name}/infer"

#Load the scaler
import pickle
with open('artifact/scaler.pkl', 'rb') as handle:
    scaler = pickle.load(handle)


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

# Get all items
@app.route('/', methods=['GET'])
def check_fraud():

    data = [0.3111400080477545, 1.9459399775518593, 1.0, 0.0, 0.0]
    prediction = rest_request(scaler.transform([data]).tolist()[0])
    
    threshhold = 0.95

    message = ''
    if (prediction[0] > threshhold):
        message = 'fraud'
    else:
        message = 'not fraud'
    return jsonify({'message': message})



# Sample data
items = [
    {'id': 1, 'name': 'Item 1', 'description': 'This is item 1'},
    {'id': 2, 'name': 'Item 2', 'description': 'This is item 2'}
]

# Get all items
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify({'items': items})


if __name__ == '__main__':
    app.run(debug=True, port=5000)