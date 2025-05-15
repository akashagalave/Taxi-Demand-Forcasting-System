import joblib
import dagshub
import mlflow
import pandas as pd
import streamlit as st
from pathlib import Path
import datetime as dt
from sklearn.pipeline import Pipeline
from sklearn import set_config
from time import sleep
import os  # Import the os module for filesystem operations

set_config(transform_output="pandas")

import dagshub
dagshub.init(repo_owner='akashagalaveaaa1', repo_name='Taxi-Demand-Prediction-System', mlflow=True)

# set the dagshub tracking server
mlflow.set_tracking_uri("https://dagshub.com/akashagalaveaaa1/Taxi-Demand-Prediction-System.mlflow")

# get model name
registered_model_name = 'uber_demand_prediction_model'
stage = "Production"
model_path = f"models:/{registered_model_name}/{stage}"

# load the latest model from model registry
model = mlflow.sklearn.load_model(model_path)

# set the root path
root_path = Path(__file__).parent
# path of the data
plot_data_path = 'data/external/plot_data.csv'
data_path = root_path / "data/processed/test.csv"

# model paths
kmeans_path = root_path / "models/mb_kmeans.joblib"
scaler_path = root_path / "models/scaler.joblib"
encoder_path = root_path / "models/encoder.joblib"
model_path = root_path / "models/model.joblib"

# load the objects
scaler = joblib.load(scaler_path)
encoder = joblib.load(encoder_path)
model = joblib.load(model_path)
kmeans = joblib.load(kmeans_path)

# --- DEBUGGING CODE ---
st.subheader("Debugging File System")
st.write("Current Working Directory:", os.getcwd())
st.write("Contents of /app directory:", os.listdir('/app'))
st.write("Contents of /app/data directory (if it exists):", os.listdir('/app/data') if os.path.exists('/app/data') else "Directory not found")
st.write("Contents of /app/data/external directory (if it exists):", os.listdir('/app/data/external') if os.path.exists('/app/data/external') else "Directory not found")
# --- END DEBUGGING CODE ---

# dataset to plot
df_plot = pd.read_csv(plot_data_path)
df = pd.read_csv(data_path, parse_dates=["tpep_pickup_datetime"]).set_index("tpep_pickup_datetime")

# ... rest of your Streamlit app code ...