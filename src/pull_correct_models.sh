#!/bin/bash

# Database connection details
DB_NAME="norm_db_00"
DB_USER="postgres"
DB_HOST="postgres-db"  # This matches the container_name in the docker-compose.yaml for the database
DB_PORT="5432"

# Directory to clone models
MODELS_DIR="./models_repo"

# Query the database to fetch mappings
echo "Fetching machine-sensor-model mappings from database..."
mappings=$(psql -U $DB_USER -h $DB_HOST -p $DB_PORT -d $DB_NAME -t -c "
  SELECT msm.machine_id, msm.sensor_id, m.model_name, m.model_repository_url, m.model_branch, m.commit_hash
  FROM machine_sensor_model_mapping msm
  JOIN model m ON msm.model_id = m.model_id;
")

# Loop through each mapping
while IFS='|' read -r machine_id sensor_id model_name repo_url branch commit_hash; do
  # Parse the mapping details
  echo "Processing: Machine ID: $machine_id, Sensor ID: $sensor_id, Model: $model_name, Commit : $commit_hash"

  # Trim whitespace
  machine_id=$(echo $machine_id | xargs)
  sensor_id=$(echo $sensor_id | xargs)
  model_name=$(echo $model_name | xargs)
  repo_url=$(echo $repo_url | xargs)
  branch=$(echo $branch | xargs)
  commit_hash=$(echo $commit_hash | xargs)

  # Clone the model repository and checkout the specific branch/commit
  if [ ! -d "$MODELS_DIR" ]; then
  git clone $repo_url "$MODELS_DIR"
  fi
  cd "$MODELS_DIR"
  # git fetch
  # git checkout $branch
  git checkout $commit_hash
  cd -
done <<< "$mappings"


echo "All models have been pulled successfully."
