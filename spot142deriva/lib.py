import pandas as pd
import numpy as np
import requests
from spot142deriva.distance import haversine
import folium
from streamlit_folium import folium_static
import streamlit as st
from datetime import datetime, timedelta

def get_data(token):
    time_now = (datetime.utcnow() + timedelta(days=1)).strftime('%Y-%m-%d')
    start_time = '2021-10-20'
    url=f'https://api.sofarocean.com/api/latest-data?spotterId=SPOT-1442&token={token}'

    response = requests.get(url).json()
    df = pd.DataFrame(response['data']['track'])
    df.rename(columns={"timestamp": "date_time"}, inplace=True)
    for i in df.columns:
        try:
            df[i] = pd.to_numeric(df[i])
        except:
            pass
    df['date_time'] = pd.to_datetime(df['date_time'], format='%Y-%m-%dT%H:%M:%S.000Z')
    df.sort_values('date_time', inplace=True)

    return df

def calculate_distance(df):
    coordinates = []
    for index, row in df.iterrows():
        coordinate = [row['latitude'], row['longitude']]
        coordinates.append(coordinate)


    deployment_loc = [-62.291317, -58.556767]
    df['coordinates'] = coordinates

    df['distance'] = df.apply(lambda row: haversine(row, deployment_loc[1], deployment_loc[0]), axis=1)

    df['veloc'] = df['distance'].diff()/(df['date_time'].diff().dt.total_seconds()/3600)
    
    return df

def plot_map(df):

    deployment_loc = [-62.291317, -58.556767]

    m = folium.Map(location=deployment_loc, zoom_start=9)

    for index, row in df.iterrows():
        popup = str(row['date_time']) + ' - veloc ' + str(round(row['veloc'],3)) + 'nós, LAT:' + str(round(row['latitude'],4))  + ', LON:' + str(round(row['longitude'],4))
        folium.Marker(row['coordinates'], tooltip=popup).add_to(m)

    folium.Marker(
        df['coordinates'].iloc[-1],
        tooltip=popup,
        icon=folium.Icon(icon_color="red", color='red')
    ).add_to(m)

    folium.Circle(deployment_loc, radius=1600).add_to(m)
    folium_static(m)

if __name__ == "__main__":
    df = get_data()

    df = calculate_distance(df)
    
    plot_map(df)
    