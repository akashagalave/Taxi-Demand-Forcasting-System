# set up the base image
FROM python:3.12.7

# set the working directory
WORKDIR /app/

# copy the requirements file to workdir
COPY requirements-docker.txt .

# install the requirements
RUN pip install -r requirements-docker.txt

# create data directories
RUN mkdir -p data/external
RUN mkdir -p data/processed
RUN mkdir models

# copy the data files
COPY ./data/external/plot_data.csv ./data/external/
COPY ./data/processed/test.csv ./data/processed/

# copy the models
COPY ./models/ ./models/

# copy the code files
COPY ./app.py ./

# expose the port on the container
EXPOSE 8000

# run the streamlit app
CMD [ "streamlit", "run", "app.py", "--server.port", "8000", "--server.address", "0.0.0.0"]