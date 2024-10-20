import torch
import tensorflow as tf
import argparse
import yaml
import json
import os
import sys
import importlib
import inspect

# Add the path to the cloned model builder repo to the Python path
sys.path.insert(0, os.path.abspath("models_repo/src"))

# Argument parsing to take the config file path
parser = argparse.ArgumentParser(description="Run inference with the pulled model")
parser.add_argument('--config', required=True, help="Path to the configuration file")
args = parser.parse_args()

# Load the configuration
with open(args.config, "r") as f:
    config = yaml.safe_load(f)

# Check for the model type: PyTorch or Keras, by inspecting the files
model_type = None
model_class = None

if os.path.exists("models/model.pt"):  # If PyTorch model
    model_type = 'pytorch'
elif os.path.exists("models/model.h5"):  # If Keras model
    model_type = 'keras'
else:
    raise ValueError("No supported model file found (model.pt for PyTorch or model.h5 for Keras)")

# Load the appropriate model based on the detected model type
if model_type == 'pytorch':
    print("Detected PyTorch model. Loading PyTorch model...")

    # Dynamically import the model module
    model_module = importlib.import_module('models')  # Import models.py dynamically

    # Automatically find the class that inherits from torch.nn.Module
    for name, obj in inspect.getmembers(model_module):
        if inspect.isclass(obj) and issubclass(obj, torch.nn.Module) and obj != torch.nn.Module:
            model_class = obj
            break

    if model_class is None:
        raise ValueError("No class inheriting from torch.nn.Module found in models.py")

    # Load the PyTorch model
    model = torch.load("models/model.pt")
    print(f"Running inference with model version: {model.get_version()}")

elif model_type == 'keras':
    print("Detected Keras model. Loading Keras model...")

    # Load the Keras model
    model = tf.keras.models.load_model("models/model.h5")
    print("Running inference with Keras model.")

# Dynamically import the preprocess and postprocess functions
preprocess_module = importlib.import_module('preprocess')
postprocess_module = importlib.import_module('postprocess')
preprocess_fn = getattr(preprocess_module, 'preprocess_audio_data')
postprocess_fn = getattr(postprocess_module, 'postprocess_anomaly_detection')

# Preprocess the input data and convert it to a tensor
input_data = preprocess_fn("data/input/dummy_data.npy")

# Process input data differently depending on the model type
if model_type == 'pytorch':
    input_tensor = torch.tensor(input_data).float()

    # Downsample or reshape the input to match the model's expected size (adjust based on model definition)
    input_tensor = input_tensor.view(1600, 10).mean(dim=0).view(1, 10)

    # Forward pass through the PyTorch model
    output = model(input_tensor)

elif model_type == 'keras':
    input_tensor = tf.convert_to_tensor(input_data, dtype=tf.float32)

    # Keras models often expect (batch_size, input_size), so reshape if needed
    input_tensor = tf.reshape(input_tensor, (1, -1))

    # Forward pass through the Keras model
    output = model(input_tensor)

# Post-process the model's output using the function from postprocess.py
result = postprocess_fn(output, config)

# Ensure the predictions directory exists
os.makedirs(os.path.dirname(config["output_file"]), exist_ok=True)

# Save the results to the output file
with open(config["output_file"], "w") as f:
    json.dump(result, f)

print(f"Inference completed. Results saved to {config['output_file']}")
