import os
import pickle
import joblib
from flask import Flask, request, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
import numpy as np

# Initialize the Flask app
app = Flask(__name__)

model = joblib.load(os.path.join(os.environ["SM_MODEL_DIR"], "model.joblib"))

# model_path = os.path.join('/opt/ml/model', 'model.pkl')
# model_path = "model/model.pkl"

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

# Load the pre-trained model from file
# with open(model_path, 'rb') as model_file:
#     model = pickle.load(model_file)

# Define the route for inference requests
@app.route('/invocations', methods=['POST'])
def predict():
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
        return "Healthy", 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
