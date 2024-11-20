#!/bin/bash

# Database connection details
DB_NAME="norm_db_00"
DB_USER="postgres"
DB_HOST="localhost"
DB_PORT="5432"

# Directory to clone models
MODELS_DIR="./models"

# Query the database to fetch mappings
echo "Fetching machine-sensor-model mappings from database..."
mappings=$(psql -U $DB_USER -d $DB_NAME -h $DB_HOST -p $DB_PORT -t -c "
    SELECT msm.machine_id, msm.sensor_id, m.model_name, m.model_repository_url, m.model_branch, m.commit_hash
    FROM machine_sensor_model_mapping msm
    JOIN model m ON msm.model_id = m.model_id;
")

# Loop through each mapping
while IFS= read -r mapping; do
    # Parse the mapping details
    IFS="|" read -r machine_id sensor_id model_name repo_url branch commit_hash <<< "$mapping"
    
    # Trim whitespace
    machine_id=$(echo $machine_id | xargs)
    sensor_id=$(echo $sensor_id | xargs)
    model_name=$(echo $model_name | xargs)
    repo_url=$(echo $repo_url | xargs)
    branch=$(echo $branch | xargs)
    commit_hash=$(echo $commit_hash | xargs)
    
    echo "Processing: Machine ID: $machine_id, Sensor ID: $sensor_id, Model: $model_name"
    
    # Call pull_model.sh with required arguments
    ./pull_model.sh "$repo_url" "$branch" "$commit_hash" "$MODELS_DIR/$machine_id/$sensor_id/$model_name"
done <<< "$mappings"

echo "All models have been pulled successfully."
