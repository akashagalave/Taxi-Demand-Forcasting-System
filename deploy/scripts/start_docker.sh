#!/bin/bash
exec > /home/ubuntu/start_docker.log 2>&1

echo "Logging in to ECR..."
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 868402157267.dkr.ecr.ap-south-1.amazonaws.com

echo "Pulling Docker image..."
docker pull 868402157267.dkr.ecr.ap-south-1.amazonaws.com/taxi-demand-prediction:latest

echo "Cleaning up existing container..."
docker stop demand-prediction || true
docker rm demand-prediction || true

echo "Starting new container..."
docker run --name demand-prediction -d -p 80:8000 \
  -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
  -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
  -e DAGSHUB_USER_TOKEN=c0b55ec2a7cd91557d2cbb386b73e314cad6dd16 \
  868402157267.dkr.ecr.ap-south-1.amazonaws.com/taxi-demand-prediction:latest

echo "Running dvc pull inside the container..."
docker exec demand-prediction dvc pull

echo "Restarting container to reflect data changes..."
docker restart demand-prediction

echo "Deployment successful."
