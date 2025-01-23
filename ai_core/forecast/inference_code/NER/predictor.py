import os
import pickle
import joblib
from flask import Flask, request, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
import numpy as np

# Initialize the Flask app
app = Flask(__name__)

# model = joblib.load(os.path.join(os.environ["SM_MODEL_DIR"], "model.joblib"))

model_path = os.path.join('/opt/ml/model', 'model.pkl')
# model_path = "model/model.pkl"


# Define the route for inference requests
@app.route('/invocations', methods=['POST'])
def predictor():
    try:
        # Get input JSON from the request
        data = request.get_json()
        # Extract the features (assuming the input is a list of values)
        features = np.array(data['features'])
        # Make predictions using the model
        prediction = model.predict(features)

        # Return the prediction as JSON
        return jsonify({'predictions': prediction.tolist()})
    
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/ping', methods=['GET'])
def ping():
    try:
        return Response(response= '\n', status=200, mimetype='application/json')
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
