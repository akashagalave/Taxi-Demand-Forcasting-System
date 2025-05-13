#!/bin/bash

# Ensure that the script runs in non-interactive mode
export DEBIAN_FRONTEND=noninteractive

# Update the package lists
sudo apt-get update -y

# Install Docker
sudo apt-get install -y docker.io

# Start and enable Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Install necessary utilities
sudo apt-get install -y unzip curl git python3-pip

# Install DVC (system-wide or in venv)
pip3 install dvc[s3]  # or dvc[gdrive], dvc[gs], etc., based on your remote

# Download and install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/home/ubuntu/awscliv2.zip"
unzip -o /home/ubuntu/awscliv2.zip -d /home/ubuntu/
sudo /home/ubuntu/aws/install

# Add ubuntu user to docker group
sudo usermod -aG docker ubuntu

# Pull DVC data (important step!)
cd /home/ubuntu/app
dvc pull -r origin || echo "DVC pull failed"

# Clean up the AWS CLI installation files
rm -rf /home/ubuntu/awscliv2.zip /home/ubuntu/aws
