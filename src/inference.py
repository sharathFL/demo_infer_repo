import torch
import argparse
import yaml
import numpy as np
import json

# Argument parsing to take the config file path
parser = argparse.ArgumentParser(description="Run inference with the pulled model")
parser.add_argument('--config', required=True, help="Path to the configuration file")
args = parser.parse_args()

# Load the configuration
with open(args.config, "r") as f:
    config = yaml.safe_load(f)

# Load the model
model = torch.load("models/model.pt")
print("Model loaded successfully")

# Load the prepared dummy input data
input_data = np.load(config["input_data"])
input_tensor = torch.tensor(input_data).float()

# Run inference
output = model(input_tensor)

# Post-process and output the results
result = {"anomaly_score": output.item(), "is_anomalous": output.item() > config["threshold"]}
with open(config["output_file"], "w") as f:
    json.dump(result, f)

print(f"Inference completed. Results saved to {config['output_file']}")
