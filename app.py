import os
import joblib
import mlflow
import pandas as pd
import streamlit as st
from pathlib import Path
import datetime as dt
from sklearn.pipeline import Pipeline
from sklearn import set_config
from time import sleep

set_config(transform_output="pandas")

# Initialize dagshub only if not disabled by env variable
if os.environ.get("DAGSHUB_DISABLE_INIT", "0") != "1":
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
model_path_local = root_path / "models/model.joblib"

# load the objects
scaler = joblib.load(scaler_path)
encoder = joblib.load(encoder_path)
model_local = joblib.load(model_path_local)
kmeans = joblib.load(kmeans_path)

# dataset to plot
df_plot = pd.read_csv(plot_data_path)
df = pd.read_csv(data_path, parse_dates=["tpep_pickup_datetime"]).set_index("tpep_pickup_datetime")

# UI of app
st.title("Uber Demand in New York City 🚕🌆")

st.sidebar.title("Options")
map_type = st.sidebar.radio(
    label="Select the type of Map",
    options=["Complete NYC Map", "Only for Neighborhood Regions"],
    index=1
)

st.subheader("Date")
date = st.date_input(
    "Select the date", 
    value=None,
    min_value=dt.date(year=2016, month=3, day=1),
    max_value=dt.date(year=2016, month=3, day=31)
) 
st.write("**Date:**", date)

st.subheader("Time")
time = st.time_input("Select the time", value=None)
st.write("**Current Time:**", time)

if date and time:
    delta = dt.timedelta(minutes=15)
    next_interval = dt.datetime(year=date.year, month=date.month, day=date.day, hour=time.hour, minute=time.minute) + delta
    st.write("Demand for Time: ", next_interval.time())

    index = pd.Timestamp(f"{date} {next_interval.time()}")
    st.write("**Date & Time:**", index)
    
    st.subheader("Location")
    sample_loc = df_plot.sample(1).reset_index(drop=True)
    lat = sample_loc["pickup_latitude"].item()
    long = sample_loc["pickup_longitude"].item()
    region = sample_loc["region"].item()
    st.write("**Your Current Location**")
    st.write(f"Lat: {lat}")
    st.write(f"Long: {long}")
    
    with st.spinner("Fetching your Current Region"):
        sleep(3)
        
    st.write("Region ID: ", region)
    scaled_cord = scaler.transform(sample_loc.iloc[:, 0:2])
    
    st.subheader("MAP")
    
    colors = ["#FF0000", "#FF4500", "#FF8C00", "#FFD700", "#ADFF2F", 
              "#32CD32", "#008000", "#006400", "#00FF00", "#7CFC00", 
              "#00FA9A", "#00FFFF", "#40E0D0", "#4682B4", "#1E90FF", 
              "#0000FF", "#0000CD", "#8A2BE2", "#9932CC", "#BA55D3", 
              "#FF00FF", "#FF1493", "#C71585", "#FF4500", "#FF6347", 
              "#FFA07A", "#FFDAB9", "#FFE4B5", "#F5DEB3", "#EEE8AA"]

    region_colors = {region: colors[i] for i, region in enumerate(df_plot["region"].unique().tolist())}
    df_plot["color"] = df_plot["region"].map(region_colors)

    pipe = Pipeline([
        ('encoder', encoder),
        ('reg', model_local)
    ])

    if map_type == "Complete NYC Map":
        progress_bar = st.progress(value=0, text="Operation in progress. Please wait.")
        for percent_complete in range(100):
            sleep(0.05)
            progress_bar.progress(percent_complete + 1, text="Operation in progress. Please wait.")
        
        st.map(data=df_plot, latitude="pickup_latitude", 
               longitude="pickup_longitude", size=0.01,
               color="color")
        progress_bar.empty()
        
        input_data = df.loc[index, :].sort_values("region")
        target = input_data["total_pickups"]
        predictions = pipe.predict(input_data.drop(columns=["total_pickups"]))

        st.markdown("### Map Legend")
        for ind in range(0,30):
            color = colors[ind]
            demand = predictions[ind]
            if region == ind:
                region_id = f"{ind} (Current region)"
            else:
                region_id = ind
            st.markdown(
                f'<div style="display: flex; align-items: center;">'
                f'<div style="background-color:{color}; width: 20px; height: 10px; margin-right: 10px;"></div>'
                f'Region ID: {region_id} <br>'
                f"Demand: {int(demand)} <br> <br>", unsafe_allow_html=True
            )
    elif map_type == "Only for Neighborhood Regions":
        distances = kmeans.transform(scaled_cord).values.ravel().tolist()
        distances = list(enumerate(distances))
        sorted_distances = sorted(distances, key=lambda x: x[1])[0:9]
        indexes = sorted([ind[0] for ind in sorted_distances])

        df_plot_filtered = df_plot[df_plot["region"].isin(indexes)]

        progress_bar = st.progress(value=0, text="Operation in progress. Please wait.")
        for percent_complete in range(100):
            sleep(0.05)
            progress_bar.progress(percent_complete + 1, text="Operation in progress. Please wait.")

        st.map(data=df_plot_filtered, latitude="pickup_latitude", 
               longitude="pickup_longitude", size=0.01,
               color="color")

        progress_bar.empty()

        input_data = df.loc[index, :]
        input_data = input_data.loc[input_data["region"].isin(indexes), :].sort_values("region")
        target = input_data["total_pickups"]

        predictions = pipe.predict(input_data.drop(columns=["total_pickups"]))

        st.markdown("### Map Legend")
        for ind in range(0,9):
            color = colors[indexes[ind]]
            demand = predictions[ind]
            if region == indexes[ind]:
                region_id = f"{indexes[ind]} (Current region)"
            else:
                region_id = indexes[ind]
            st.markdown(
                f'<div style="display: flex; align-items: center;">'
                f'<div style="background-color:{color}; width: 20px; height: 10px; margin-right: 10px;"></div>'
                f'Region ID: {region_id} <br>'
                f"Demand: {int(demand)} <br> <br>", unsafe_allow_html=True
            )
