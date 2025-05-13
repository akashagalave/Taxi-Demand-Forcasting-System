# set up the base image
FROM python:3.12.7

# set the working directory
WORKDIR /app/

# copy requirements and install
COPY requirements-docker.txt .
RUN pip install --upgrade pip && pip install -r requirements-docker.txt

# install DVC with S3 support
RUN pip install dvc[s3]

# copy everything including DVC metadata and tracked files
COPY . .

# make sure you're inside a DVC repo now
RUN dvc pull && dvc checkout

# expose port and run Streamlit
EXPOSE 8000
CMD ["streamlit", "run", "app.py", "--server.port", "8000", "--server.address", "0.0.0.0"]
