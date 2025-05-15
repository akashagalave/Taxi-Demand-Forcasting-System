#!/bin/bash
exec > /home/ubuntu/start_docker.log 2>&1

echo "Cleaning up old Docker containers and images..."
docker system prune -af

echo "Logging in to Amazon ECR..."
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 868402157267.dkr.ecr.ap-south-1.amazonaws.com

echo "Pulling latest Docker image..."
docker pull 868402157267.dkr.ecr.ap-south-1.amazonaws.com/taxi-demand-prediction:latest

echo "Stopping existing container..."
docker stop taxi-demand-container || true
docker rm taxi-demand-container || true

echo "Running new container..."
docker run -d \
  --name taxi-demand-container \
  -p 80:80 \
  -w /app \
  868402157267.dkr.ecr.ap-south-1.amazonaws.com/taxi-demand-prediction:latest \
  streamlit run app.py

echo "Deployment completed successfully."