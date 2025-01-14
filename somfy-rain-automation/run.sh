#!/bin/bash

# Script to build and run the Somfy Rain Automation Docker container

# --- Configuration ---
IMAGE_NAME="somfy-rain-automation"
CONTAINER_NAME="somfy-app"
ENV_FILE=".env"

# --- Functions ---

# Build the Docker image
build_image() {
  echo "Building Docker image: $IMAGE_NAME..."
  docker build -t "$IMAGE_NAME" .
  if [ $? -eq 0 ]; then
    echo "Image built successfully."
  else
    echo "Error building image."
    exit 1
  fi
}

# Stop and remove existing container (if any)
stop_container() {
  if docker ps -q --filter "name=$CONTAINER_NAME" | grep -q .; then
    echo "Stopping existing container: $CONTAINER_NAME..."
    docker stop "$CONTAINER_NAME"
    if [ $? -eq 0 ]; then
      echo "Container stopped."
    else
      echo "Error stopping container."
      exit 1
    fi
  fi

  if docker ps -aq --filter "name=$CONTAINER_NAME" | grep -q .; then
    echo "Removing existing container: $CONTAINER_NAME..."
    docker rm "$CONTAINER_NAME"
    if [ $? -eq 0 ]; then
      echo "Container removed."
    else
      echo "Error removing container."
      exit 1
    fi
  fi
}

# Run the Docker container
run_container() {
  echo "Running Docker container: $CONTAINER_NAME..."
  docker run -d \
    --name "$CONTAINER_NAME" \
    --env-file "$ENV_FILE" \
    "$IMAGE_NAME"
  if [ $? -eq 0 ]; then
    echo "Container started successfully."
  else
    echo "Error starting container."
    exit 1
  fi
}

# --- Main Script ---

# Build the image
build_image

# Stop and remove any old container
stop_container

# Run the new container
run_container

echo "Done."
exit 0