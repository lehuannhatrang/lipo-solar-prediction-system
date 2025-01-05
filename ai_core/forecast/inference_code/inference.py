import pickle
from flask import Flask, request, jsonify
import numpy as np

# Initialize the Flask app
app = Flask(__name__)

# Load the pre-trained model from file
with open('model/model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Define the route for inference requests
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input JSON from the request
        data = request.get_json()
        # Extract the features (assuming the input is a list of values)
        features = np.array(data['features']).reshape(1, -1)
        
        # Make predictions using the model
        prediction = model.predict(features)

        # Return the prediction as JSON
        return jsonify({'prediction': prediction[0]})
    
    except Exception as e:
        return jsonify({'error': str(e)})

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
