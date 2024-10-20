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

# Get the model repo URL, branch, and model filename from config.yaml
MODEL_REPO_URL = config['model_repo_url']
MODEL_BRANCH = config['model_branch']
MODEL_FILENAME = config['model_filename']  # The model filename is specified in the config

# Step 1: Clone the model builder repository if it doesn't exist
if not os.path.exists("models_repo"):
    print(f"Cloning {MODEL_REPO_URL} into models_repo directory...")
    subprocess.run(["git", "clone", MODEL_REPO_URL, "models_repo"], check=True)

# Step 2: Checkout the correct branch
print(f"Checking out branch {MODEL_BRANCH} in models_repo...")
subprocess.run(["git", "-C", "models_repo", "checkout", MODEL_BRANCH], check=True)

# Step 3: Pull the model from the DVC remote storage (ensure DVC is initialized in the model repo)
print("Pulling model from DVC...")
subprocess.run(["dvc", "pull"], cwd="models_repo", check=True)

# Step 4: Use the model filename from the config file
model_src_path = os.path.join("models_repo", "models", MODEL_FILENAME)
model_dst_path = os.path.join("models", "model.pt")

# Step 5: Copy the model and preprocessing scripts to the correct locations in the inference repo
os.makedirs("models", exist_ok=True)

if os.path.exists(model_src_path):
    subprocess.run(["cp", model_src_path, model_dst_path], check=True)
    print(f"Model {MODEL_FILENAME} from branch {MODEL_BRANCH} successfully pulled and copied to the inference repo.")
else:
    raise FileNotFoundError(f"Model file '{MODEL_FILENAME}' not found in models_repo/models/")

