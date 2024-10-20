import os
import subprocess
import argparse
import yaml

# Argument parsing to take the config file path
parser = argparse.ArgumentParser(description="Pull the correct model based on the branch and model repo URL")
parser.add_argument('--config', required=True, help="Path to the configuration file")
args = parser.parse_args()

# Load the configuration from config.yaml
with open(args.config, "r") as f:
    config = yaml.safe_load(f)

# Get the model repo URL and branch from config.yaml
MODEL_REPO_URL = config['model_repo_url']
MODEL_BRANCH = config['model_branch']

# Step 1: Clone the model builder repository if it doesn't exist
if not os.path.exists("models_repo"):
    subprocess.run(["git", "clone", MODEL_REPO_URL, "models_repo"])

# Step 2: Checkout the correct branch
subprocess.run(["git", "-C", "models_repo", "checkout", MODEL_BRANCH])

# Step 3: Pull the model using DVC from the correct branch
subprocess.run(["dvc", "-C", "models_repo", "pull"])

# Step 4: Copy the model to the inference repo
subprocess.run(["cp", "models_repo/models/model.pt", "models/model.pt"])

print(f"Model from branch {MODEL_BRANCH} successfully pulled and copied to the inference repo.")
