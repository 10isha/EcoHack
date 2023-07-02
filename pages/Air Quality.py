# Required Libraries
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import dates
from datetime import datetime
from matplotlib import rcParams
from API import owm
import plotly.express as px
from pyowm.commons.exceptions import NotFoundError
import pandas as pd
import plotly.express as px
import joblib


# Streamlit Display
st.set_page_config(layout="centered")
st.title(" 📅 Find your Air Quality 🌥️ ☔ ")


st.header("🌐 Enter the name of City")
place = st.text_input("NAME OF THE CITY 🌆 ", " ")
b = st.button("SUBMIT")

# To deceive error of pyplot global warning
st.set_option('deprecation.showPyplotGlobalUse', False)


def mapping(aqi):
    if aqi>=0 and aqi<=50:
        return "Good"
    elif aqi>=51 and aqi<=100:
        return "Satisfactory"
    elif aqi>=101 and aqi<=200:
        return "Moderate"
    elif aqi>=201 and aqi<=300:
        return "Poor"
    elif aqi>=301 and aqi<=400:
        return "Very Poor"
    else:
        return "Severe"

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
    X = [[air_status.pm2_5,air_status.pm10,air_status.no,air_status.no2,32.448956,air_status.nh3,air_status.co,air_status.so2,air_status.o3,3.700361,10.323696,2.557439]]
    loaded_model = joblib.load('model_Air.sav')
    answer = loaded_model.predict(X)
    st.title(f"📍Air Quality {place[0].upper() + place[1:]} currently: ")
    aqi = answer[0]
    st.write(f"## AQI Predicted by our Model: {int(aqi)} , {mapping(aqi)}")
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



