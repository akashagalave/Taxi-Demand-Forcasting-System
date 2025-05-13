FROM python:3.12.7

WORKDIR /app/

COPY requirements-docker.txt .

# Install Python dependencies and DVC
RUN pip install --upgrade pip && pip install -r requirements-docker.txt

# Copy the rest of the repo (including .dvc files)
COPY . .

# Pull DVC data (ensure you have DVC installed in requirements)
# You can use the environment variables set in the CI/CD pipeline or local machine
RUN dvc pull -r origin

# Expose port and run Streamlit
EXPOSE 8000

CMD ["streamlit", "run", "app.py", "--server.port", "8000", "--server.address", "0.0.0.0"]
