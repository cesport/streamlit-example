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
