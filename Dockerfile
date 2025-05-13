# set up the base image
FROM python:3.12.7

# set the working directory
WORKDIR /app/

# copy requirements first and install them
COPY requirements-docker.txt .
RUN pip install -r requirements-docker.txt

# copy everything (code, models, DVC metadata, etc.)
COPY . .

# pull DVC data from remote
RUN dvc pull && dvc checkout

# expose the port on the container
EXPOSE 8000

# run the streamlit app
CMD ["streamlit", "run", "app.py", "--server.port", "8000", "--server.address", "0.0.0.0"]
