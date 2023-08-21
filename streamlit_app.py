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

# SIDEBAR ============================================================
## Description box
### Add description to the sidebar
st.sidebar.header('Description')
st.sidebar.info('This is the description for the performance dashboard. Lorem ipsum dolor sit amet, \
consectetur adipiscing elit. Ut in vestibulum nisi, et blandit neque. Vestibulum ipsum nibh, \
consectetur in fermentum et, ornare in justo. Proin pulvinar sagittis porta. Nullam metus orci, interdum et diam sed.', icon="ℹ️")

## Slider
### Start and end dates for the time period slider
start_date = dt.date(year=2023,month=1,day=1)
end_date = dt.date(year=2023,month=4,day=15)

### Add a slider to the sidebar:
st.sidebar.header('Time period')
timerange=st.sidebar.slider(
  label='Please select an interval:',
  min_value=start_date,
  max_value=end_date,
  value=(start_date, end_date),
  format='MMM YY',
  step=dt.timedelta(days=1)
)

## Selection box
### Add a selectbox to the sidebar:
st.sidebar.header('Origin airport selection')
st.sidebar.selectbox(
    label='Focus:',
    options=('CDG', 'JFK', 'NRT')
)

## Radio buttons
### Add radio buttons
st.sidebar.write('Benchmarks:')
st.sidebar.checkbox('CDG')
st.sidebar.checkbox('JFK')
st.sidebar.checkbox('NRT')

## Additional information
st.sidebar.header('Data source details')
st.sidebar.write('These are the data source details. Lorem ipsum dolor sit amet, \
consectetur adipiscing elit. Ut in vestibulum nisi, et blandit neque. Vestibulum ipsum nibh, \
consectetur in fermentum et, ornare in justo. Proin pulvinar sagittis porta. Nullam metus orci, interdum et diam sed.')

# TAB Settings =============================================================
## set tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Performance", "Carriers", "Flights", "Fares", "Cargo"])

# PERFORMANCE TAB =============================================================
## Initialize tab 1
with tab1:
  ### Column definition
  col1, col2 = st.columns(2)
  ### Reading exported data (txt file in repo, exported from Google Colab using Pickle)
  with open('sample.txt', 'rb') as f:
    total, airlines, complete, bystate, carrierp, paxcargo=pd.read_pickle(f)
    
  #### Initialize column 1
  with col1:
    st.subheader("Cancellations")
    ##### Define subtabs inside column 1
    subtab1, subtab2, subtab3 = st.tabs(['Total','Per airline', 'Geographic'])

    ##### Create line chart for total cancellations
    subtab1.write("Total number of flight cancelled per month")
    new_total=total[total.index >= str(timerange[0].month)]
    new_total=new_total[new_total.index <= str(timerange[1].month+1)]
    subtab1.line_chart(data=new_total)
    
    ##### Create line chart for cancellations per airline (for American, Delta & Southwest for now)
    subtab2.write("Volume of cancellations by carrier")
    new_airlines=airlines[airlines.index >= str(timerange[0].month)]
    new_airlines=new_airlines[new_airlines.index <= str(timerange[1].month+1)]
    subtab2.line_chart(data=new_airlines)

    ##### Map for volume of cancellations by destination
    subtab3.write("Volume of cancellations by destination")
    ###### Filter dataset according to time period
    new_bystate=bystate[bystate.Month>=timerange[0].month]
    new_bystate=new_bystate[new_bystate.Month<=timerange[1].month]
    new_bystate=new_bystate.groupby(['DestStateName'])['Total'].agg('sum')
    new_bystate=pd.DataFrame(new_bystate)
    new_bystate.reset_index(inplace=True)
    ###### Create map object, uses geojson file located in the repo
    map = folium.Map(location=[38, -96.5], zoom_start=3, scrollWheelZoom=False, tiles='CartoDB positron')
    choropleth = folium.Choropleth(
        geo_data='us-state-boundaries.geojson',
        data=new_bystate,
        columns=('DestStateName', 'Total'),
        key_on='feature.properties.name',
        line_opacity=0.8,
        highlight=True)
    choropleth.geojson.add_to(map)
    ###### Create text bubble that appears when hovering over states in the map
    df_indexed = new_bystate.set_index('DestStateName')
    for feature in choropleth.geojson.data['features']:
      state_name = feature['properties']['name']
      feature['properties']['cancelled'] = 'Cancelled flights: ' + '{:,}'.format(df_indexed.loc[state_name, 'Total']) if state_name in list(df_indexed.index) else ''
      feature['properties']['timeframe'] = 'Time period: {} - {}'.format(timerange[0].strftime("%m/%y"), timerange[1].strftime("%m/%y"))
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['name', 'cancelled', 'timeframe'], labels=False))
    ###### Add map to the dashboard
    with subtab3:
      folium_static(map, width=300, height=300)

  #### Initialize column 2
  col2.subheader("Taxi time")
  ##### Query taxi time dataset based on time constraints
  complete_new=complete.query('{} <= Month <= {}'.format(timerange[0].month, timerange[1].month))
  ##### Create scatter plot, continous variables are specified in 4 fields: x, y, size & color; logarithmic scale can be turned off in the field log_x
  fig = px.scatter(
      complete_new,
      x="TaxiOut",
      y="DepDelay",
      size="Distance",
      color="Month",
      hover_name="Operating_Airline ",
      log_x=True,
      size_max=60,
  )
  ##### Add scatter plot to the dashboard 
  col2.plotly_chart(fig, theme="streamlit", use_container_width=True)

  ### Definition of columns 3 & 4 (below 1 & 2)
  col3, col4 = st.columns(2)

  #### Initialize column 3
  col3.subheader("Carrier presence")
  ##### Create bar chart of carrier presence for column 3
  fig=px.bar(carrierp,x='Counts',y=carrierp.index, orientation='h')
  col3.plotly_chart(fig, theme="streamlit", use_container_width=True)

  #### Initialize column 4
  with col4:
    st.subheader("Volume")
    ##### Add line chart related to PAS & Cargo stats
    st.line_chart(paxcargo)

    ###### Intialize two secondary columns for metrics
    subcol1, subcol2= st.columns([1,1])

    ###### Add metrics (right now placeholders) 
    subcol1.metric("PAX yearly delta", "1500", "-31%")
    subcol2.metric("Cargo yearly delta", "1200 lb", "15%")

# ADDITIONAL TABS =============================================================
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
