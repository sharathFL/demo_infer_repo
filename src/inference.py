import importlib.util
import os
import torch
import joblib
import pandas as pd

import sys
import os

from models_repo.src.models.base_model import BaseModel

# Add models_repo/src to the system path
sys.path.append("/code/src/models_repo/src")


# Define paths for dynamic imports
models_repo_path = "/code/src/models_repo/src"
trained_model_path= "/code/src/models_repo/trained_models/model.pt"
model_meta_path='/code/src/models_repo/trained_models/model_meta.json'


model_meta=BaseModel.load_model_meta(model_meta_path)
print(model_meta)

# Dynamically load the class
class_name = model_meta.get('class_name')
# module_name = module_name = f"models.{model_meta['class_name'].lower()}"  # Assuming filenames are lowercased
module_name = f"models_repo.src.models.{model_meta['class_name'].lower()}"

model_class = getattr(importlib.import_module(module_name), class_name)

# Call the load method of the dynamically loaded class
model = model_class.load(filepath=trained_model_path)

# Define the file path for inference
file_path = "/infer_data/audio_2024_01_11_05_44_48.wav"

# Run preprocessing, prediction, and postprocessing
features = model.preprocess(file_path)
raw_prediction = model.predict(features)
print(raw_prediction)
result = model.postprocess(raw_prediction,features)

# Print the prediction result
print(f"Inference result: {result}")
# Ensure the results directory exists
os.makedirs('results', exist_ok=True)

# Sample prediction result
predictions = pd.DataFrame([{"prediction": result}])  # Replace with actual prediction logic
predictions.to_csv('results/predictions.csv', index=False)
