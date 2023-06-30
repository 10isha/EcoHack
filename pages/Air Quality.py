# Required Libraries
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import dates
from datetime import datetime
from matplotlib import rcParams
from API import owm
import plotly.express as px
from pyowm.commons.exceptions import NotFoundError
import requests
import json
import pandas as pd
import plotly.express as px
from IPython.display import display



weather_requests = requests.get(
         "http://api.openweathermap.org/data/2.5/air_pollution?lat=50&lon=50&appid=db6982460167642c1b96e97548663c4b"
    )
json_data = weather_requests.json()
df1 = pd.json_normalize(json_data)


# Streamlit Display
st.set_page_config(layout="centered")
st.title(" 📅 Find your Air Quality 🌥️ ☔ ")


st.header("🌐 Enter the name of City")
place = st.text_input("NAME OF THE CITY 🌆 ", " ")
b = st.button("SUBMIT")

# To deceive error of pyplot global warning
st.set_option('deprecation.showPyplotGlobalUse', False)


def plot_temperature(df,min_t,max_t,days):
      fig = px.bar(df,x='Days', y='Temperature')
      fig.update_layout(
      updatemenus=[
        dict(
            type="buttons",
            direction="down",
            buttons=list([
                dict(
                    args=["type", "bar"],
                    label="Bar Plot",
                    method="restyle"
                ),
                dict(
                    args=["type", "line"],
                    label="Line Chart",
                    method="restyle"
                ),
                 dict(
                    args=["type", "box"],
                    label="Box Plot",
                    method="restyle"
                )
            ]),
        ),
    ]
)
   


def display_detail(place):
    mgr = owm.airpollution_manager()
    mgr2 = owm.geocoding_manager()
    list_of_locations = mgr2.geocode(place)
    placehere = list_of_locations[0]  # taking the first London in the list
    days = []
    co =[]
    o3 =[]
    so2 = []
    dates_2=[]
    air_status = mgr.air_quality_at_coords(placehere.lat, placehere.lon)
    st.title(f"📍Air Quality {place[0].upper() + place[1:]} currently: ")
    st.write(f"## AQI: {air_status.aqi}")
    st.write(f"## CO Levels: {air_status.co} ")
    st.write(f"### Ozone Levels : {air_status.o3} ")
    st.write(f"### SO2 Levels: {air_status.so2} ")
    list_forecast = mgr.air_quality_forecast_at_coords(placehere.lat, placehere.lon)
    for air in list_forecast:
      day = datetime.utcfromtimestamp(air.reference_time())
      date1 = day.date()
      if date1 not in dates_2:
            dates_2.append(date1)
            co.append(None)
            so2.append(None)
            days.append(date1)
            o3.append(None)
      if not co[-1]:
            co[-1] = air.co
      if not so2[-1]:
            so2[-1] = air.so2
      if not o3[-1]:
            o3[-1] = air.o3
    df = pd.DataFrame(list(zip(days,co,so2,o3)),
               columns =['Days', 'CO','SO2','O3'])
    st.write('CO Levels Forecasting')
    fig1 = px.bar(df,x='Days', y='CO')
    fig1.update_layout(
      updatemenus=[
        dict(
            type="buttons",
            direction="down",
            buttons=list([
                dict(
                    args=["type", "bar"],
                    label="Bar Plot",
                    method="restyle"
                ),
                dict(
                    args=["type", "line"],
                    label="Line Chart",
                    method="restyle"
                )
            ]),
        ),
    ]
)
    st.plotly_chart(fig1, theme="streamlit")
    st.write('                ')
    st.write('SO2 Levels Forecasting')
    fig2 = px.bar(df ,x='Days', y='SO2')
    fig2.update_layout(
        updatemenus=[
        dict(
            type="buttons",
            direction="down",
            buttons=list([
                dict(
                    args=["type", "bar"],
                    label="Bar Plot",
                    method="restyle"
                ),
                dict(
                    args=["type", "line"],
                    label="Line Chart",
                    method="restyle"
                )
            ]),
        ),
    ]
)   
    st.plotly_chart(fig2, theme="streamlit")
    st.write('                ')
    st.write("O3 Levels Forecasting")
    fig3 = px.bar(df ,x='Days', y='O3')
    fig3.update_layout(
      updatemenus=[
        dict(
            type="buttons",
            direction="down",
            buttons=list([
                dict(
                    args=["type", "bar"],
                    label="Bar Plot",
                    method="restyle"
                ),
                dict(
                    args=["type", "line"],
                    label="Line Chart",
                    method="restyle"
                )
            ]),
        ),
    ]
)  
    st.plotly_chart(fig3, theme="streamlit")
   
if b:
    if place != "":
        try:
         display_detail(place)

        except NotFoundError:
            st.write("Please enter a Valid city name")



