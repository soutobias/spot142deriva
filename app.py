import streamlit as st
from spot142deriva import lib
from dotenv import load_dotenv
import os

load_dotenv()


df = lib.get_data(os.getenv('TOKEN'))

st.write("# SPOTTER POTTER DERIVA")
if df.empty:
    st.write('#### Não há dados')
else:
    st.write(f"#### {(df['date_time'].min())} até {(df['date_time'].max())}")
    st.write(f"#### Última posição: LAT {(df['latitude'].iloc[-1])}, LON {(df['longitude'].iloc[-1])}")
    df = lib.calculate_distance(df)
    lib.plot_map(df)
