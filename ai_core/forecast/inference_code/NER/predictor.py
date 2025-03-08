import os
import json
import torch
import numpy as np
from flask import Flask, Response, request, jsonify

# Initialize the Flask app
app = Flask(__name__)

# Hyperparameters from environment variables with defaults
input_size = int(os.environ.get('SM_HP_INPUT_SIZE', 3))
hidden_size = int(os.environ.get('SM_HP_HIDDEN_SIZE', 64))
num_layers = int(os.environ.get('SM_HP_NUM_LAYERS', 2))
sequence_length = int(os.environ.get('SM_HP_SEQUENCE_LENGTH', 40))
future_steps = int(os.environ.get('SM_HP_FUTURE_STEPS', 20))
batch_size = int(os.environ.get('SM_HP_BATCH_SIZE', 32))

class PredictModel(torch.nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, future_steps):
        super(PredictModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = torch.nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = torch.nn.Linear(hidden_size, future_steps)
    
    def forward(self, x):
        # Initialize hidden state with zeros
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        
        # Forward propagate LSTM
        out, _ = self.lstm(x, (h0, c0))
        
        # Decode the hidden state of the last time step
        out = self.fc(out[:, -1, :])
        return out

def model_fn(model_dir):
    """Load the PyTorch model from the `model_dir` directory."""
    try:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Initialize model with the same architecture
        model = PredictModel(input_size, hidden_size, num_layers, future_steps)
        
        # In SageMaker, the model file will be in the model_dir
        model_path = os.path.join(model_dir, "model.pt")
        if not os.path.exists(model_path):
            print(f"Warning: Model file not found at {model_path}. Using uninitialized model for development.")
            return model.to(device)
        
        # Load the saved model state_dict
        model.load_state_dict(torch.load(model_path, map_location=device))
        model.to(device)
        model.eval()
        return model
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        raise

def input_fn(request_body, content_type="application/json"):
    """Parse input data payload"""
    try:
        if content_type == "application/json":
            data = json.loads(request_body)
            if "features" not in data:
                raise ValueError("Input data must contain 'features' key")
                
            features = torch.tensor(data["features"], dtype=torch.float32)
            
            # Ensure input shape is correct (batch_size, sequence_length, input_size)
            if len(features.shape) == 2:
                features = features.unsqueeze(0)  # Add batch dimension if not present
            
            if features.shape[-1] != input_size:
                raise ValueError(f"Expected input_size of {input_size}, got {features.shape[-1]}")
            
            return features
        raise ValueError(f"Unsupported content type: {content_type}")
    except Exception as e:
        print(f"Error processing input: {str(e)}")
        raise

def predict_fn(input_data, model):
    """Make prediction using model and input data"""
    try:
        device = next(model.parameters()).device
        input_data = input_data.to(device)
        
        with torch.no_grad():
            output = model(input_data)
        return output
    except Exception as e:
        print(f"Error during prediction: {str(e)}")
        raise

def output_fn(prediction, accept="application/json"):
    """Format prediction output"""
    try:
        if accept == "application/json":
            prediction = prediction.cpu().numpy()
            response = {
                "predictions": prediction.tolist()
            }
            return json.dumps(response)
        raise ValueError(f"Unsupported accept type: {accept}")
    except Exception as e:
        print(f"Error formatting output: {str(e)}")
        raise

# Load the model on startup
# In SageMaker, the model will be in /opt/ml/model
model = model_fn(os.environ.get("SM_MODEL_DIR", "/opt/ml/model"))

@app.route("/invocations", methods=["POST"])
def predict():
    """Handle the prediction request"""
    try:
        # Get input data
        input_data = input_fn(request.get_data().decode("utf-8"), request.content_type)
        
        # Make prediction
        prediction = predict_fn(input_data, model)
        
        # Process the output
        response = output_fn(prediction, request.accept_mimetypes.best)
        
        return Response(response=response, status=200, mimetype=request.accept_mimetypes.best)
    except Exception as e:
        error_message = str(e)
        print(f"Error during inference: {error_message}")
        return jsonify({"error": error_message}), 500

@app.route("/ping", methods=["GET"])
def ping():
    """Determine if the container is working and healthy"""
    try:
        health_check = {
            "status": "Healthy" if model is not None else "Unhealthy",
            "message": "Model loaded successfully"
        }
        status_code = 200 if model is not None else 404
        return jsonify(health_check), status_code
    except Exception as e:
        return jsonify({"status": "Unhealthy", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
