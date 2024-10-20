import torch
import argparse
import yaml
import json
import os
import sys

# Add the path to the cloned model builder repo to the Python path
sys.path.insert(0, os.path.abspath("models_repo/src"))

# Import the model class and preprocessing/post-processing functions from the cloned model builder repo
from models import DummyModelV2  # Import the model class from the cloned repo
from preprocess import preprocess_audio_data  # Import the preprocessing function
from postprocess import postprocess_anomaly_detection  # Import the post-processing function

# Argument parsing to take the config file path
parser = argparse.ArgumentParser(description="Run inference with the pulled model")
parser.add_argument('--config', required=True, help="Path to the configuration file")
args = parser.parse_args()

# Load the configuration
with open(args.config, "r") as f:
    config = yaml.safe_load(f)

# Load the entire model (architecture + weights)
model = torch.load("models/model.pt")

# Print model version to confirm which model is being used
print(f"Running inference with model version: {model.get_version()}")

# Preprocess the input data and convert it to a tensor
input_data = preprocess_audio_data("data/input/dummy_data.npy")
input_tensor = torch.tensor(input_data).float()

# Downsample or reshape the input to match the model's expected size (e.g., (10, 1))
input_tensor = input_tensor.view(1600, 10).mean(dim=0).view(1, 10)

# Forward pass through the model
output = model(input_tensor)

# Post-process the model's output using the function from postprocess.py
result = postprocess_anomaly_detection(output, config)

# Ensure the predictions directory exists
os.makedirs(os.path.dirname(config["output_file"]), exist_ok=True)

# Save the results to the output file
with open(config["output_file"], "w") as f:
    json.dump(result, f)

print(f"Inference completed. Results saved to {config['output_file']}")
