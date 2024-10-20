# Base image with Python
FROM python:3.9-slim

# Set up environment
WORKDIR /workspace

# Copy only requirements.txt to leverage Docker caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the rest of the code
COPY . .

# Keep the container running for interactive DVC usage
CMD ["tail", "-f", "/dev/null"]
