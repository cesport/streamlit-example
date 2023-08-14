from collections import namedtuple
import altair as alt
import math
import pandas as pd
import numpy as np
import streamlit as st
import datetime as dt
import pickle
import plotly.express as px
import folium
from streamlit_folium import folium_static

from dateutil.relativedelta import relativedelta # to add days or years

start_date = dt.date(year=2020,month=1,day=1)
end_date = dt.date(year=2022,month=12,day=1)

# set tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Performance", "Carriers", "Flights", "Fares", "Cargo"])

# PERFORMANCE TAB =============================================================
with tab1:
  col1, col2 = st.columns(2)

  with open('sample.txt', 'rb') as f:
    total, airlines, complete, bystate, carrierp, paxcargo=pd.read_pickle(f)

  with col1:
    st.subheader("Cancellations")
    subtab1, subtab2, subtab3 = st.tabs(['Total','Per airline', 'Geographic'])

    subtab1.write("Total number of flight cancelled per month")
    subtab1.line_chart(data=total)

    subtab2.write("Volume of cancellations by carrier")
    subtab2.line_chart(data=airlines)
    subtab3.write("Volume of cancellations by destination")

    #Define map
    map = folium.Map(location=[38, -96.5], zoom_start=3, scrollWheelZoom=False, tiles='CartoDB positron')
    choropleth = folium.Choropleth(
        geo_data='us-state-boundaries.geojson',
        data=bystate,
        columns=('DestStateName', 'Total'),
        key_on='feature.properties.name',
        line_opacity=0.8,
        highlight=True)
    choropleth.geojson.add_to(map)

    df_indexed = bystate.set_index('DestStateName')
    for feature in choropleth.geojson.data['features']:
      state_name = feature['properties']['name']
      feature['properties']['cancelled'] = 'Cancelled flights: ' + '{:,}'.format(df_indexed.loc[state_name, 'Total']) if state_name in list(df_indexed.index) else ''
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['name', 'cancelled'], labels=False))
    with subtab3:
      folium_static(map, width=300, height=300)

  col2.subheader("Taxi time")
  fig = px.scatter(
      complete,
      x="TaxiOut",
      y="DepDelay",
      size="Distance",
      color="Month",
      hover_name="Operating_Airline ",
      log_x=True,
      size_max=60,
  )

  col2.plotly_chart(fig, theme="streamlit", use_container_width=True)

  col3, col4 = st.columns(2)

  col3.subheader("Carrier presence")
  col3.bar_chart(carrierp)

  with col4:
    st.subheader("Volume")
    subcol1, subcol2= st.columns([1,1])

    subcol1.line_chart(paxcargo)

    subcol2.metric("PAX yearly delta", "1500", "-31%")
    subcol2.metric("Cargo yearly delta", "1200 lb", "15%")

  #Add description to the sidebar
  st.sidebar.header('Description')
  st.sidebar.info('This is the description for the performance dashboard. Lorem ipsum dolor sit amet, \
  consectetur adipiscing elit. Ut in vestibulum nisi, et blandit neque. Vestibulum ipsum nibh, \
  consectetur in fermentum et, ornare in justo. Proin pulvinar sagittis porta. Nullam metus orci, interdum et diam sed.', icon="ℹ️")

  # Add a slider to the sidebar:
  st.sidebar.header('Time period')
  st.sidebar.slider(
  label='Please select an interval:',
  min_value=start_date,
  max_value=end_date,
  value=(start_date, end_date),
  format='MMM YY',
  step=dt.timedelta(days=1)
  )

  # Add a selectbox to the sidebar:
  st.sidebar.header('Origin airport selection')
  st.sidebar.selectbox(
      label='Focus:',
      options=('CDG', 'JFK', 'NRT')
  )

  #Add radio buttons
  st.sidebar.write('Benchmarks:')
  st.sidebar.checkbox('CDG')
  st.sidebar.checkbox('JFK')
  st.sidebar.checkbox('NRT')

  st.sidebar.header('Data source details')
  st.sidebar.write('These are the data source details. Lorem ipsum dolor sit amet, \
  consectetur adipiscing elit. Ut in vestibulum nisi, et blandit neque. Vestibulum ipsum nibh, \
  consectetur in fermentum et, ornare in justo. Proin pulvinar sagittis porta. Nullam metus orci, interdum et diam sed.')

with tab2:
   st.header("Carriers dashboard")
   st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with tab3:
   st.header("Flights dashboard")
   st.image("https://static.streamlit.io/examples/owl.jpg", width=200)

with tab4:
   st.header("Fares dashboard")
   st.image("https://static.streamlit.io/examples/owl.jpg", width=200)

with tab5:
   st.header("Cargo dashboard")
   st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
