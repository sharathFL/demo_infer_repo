import os
import argparse
import numpy as np

# Argument parsing
parser = argparse.ArgumentParser(description="Prepare dummy data for inference")
parser.add_argument('--output', required=True, help="Path to save the prepared data")
args = parser.parse_args()

# Ensure the output directory exists
os.makedirs(os.path.dirname(args.output), exist_ok=True)

# Simulate dummy audio data (e.g., 16k samples of random noise)
dummy_data = np.random.rand(16000).astype(np.float32)

# Save the dummy data as a .npy file
np.save(args.output, dummy_data)

print(f"Dummy data prepared and saved to {args.output}")
