import argparse
import yaml
import numpy as np
import os

# Argument parsing to take the config file path
parser = argparse.ArgumentParser(description="Prepare data for training")
parser.add_argument('--config', required=True, help="Path to the configuration file")
args = parser.parse_args()

# Load the configuration file to get the output path
with open(args.config, "r") as f:
    config = yaml.safe_load(f)

# Prepare dummy data
dummy_data = np.random.rand(16000).astype(np.float32)  # Generate random dummy data

# Ensure the output directory exists
output_dir = os.path.dirname(config['output'])
os.makedirs(output_dir, exist_ok=True)

# Save the dummy data to the specified output path
np.save(config['output'], dummy_data)
print(f"Dummy data prepared and saved to {config['output']}")
