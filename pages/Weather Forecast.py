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
from pyowm.tiles.enums import MapLayerEnum
from pyowm.utils.geo import Point
from pyowm.commons.tile import Tile

weather_requests = requests.get(
        "https://api.openweathermap.org/data/2.5/weather?q=indore&appid=db6982460167642c1b96e97548663c4b"
    )
json_data = weather_requests.json()
df = pd.json_normalize(json_data)


# Streamlit Display
st.set_page_config(layout="centered")
st.title(" 📅 WEATHER FORECASTER 🌥️ ☔ ")


st.header("🌐 Enter the name of City and Select Temperature Unit")
place = st.text_input("NAME OF THE CITY 🌆 ", " ")
unit = st.selectbox(" SELECT TEMPERATURE UNIT 🌡 ", ("Celsius", "Fahrenheit"))
g_type = st.selectbox("SELECT GRAPH TYPE 📉 ", ("Display Content", "Temperature Forecast","Humidity Forecast"))
b = st.button("SUBMIT")

# To deceive error of pyplot global warning
st.set_option('deprecation.showPyplotGlobalUse', False)


def plot_rain(df):
    fig = px.bar(df,x='Days', y='Humidity')
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
    st.plotly_chart(fig, theme="streamlit")
            
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
    st.plotly_chart(fig, theme="streamlit")
    i = 0
    st.write(f"# 📆 Date :  Max - Min  ({unit})")
    for obj in days:
        ta = (obj.strftime("%d/%m"))
        st.write(f'### ➡️ {ta} :\t   ({max_t[i]} - {min_t[i]})')
        i += 1


def display_detail(place, unit):
    mgr = owm.weather_manager()
    days = []
    dates_2 = []
    min_t = []
    max_t = []
    temps =[]
    forecaster = mgr.forecast_at_place(place, '3h')
    forecast = forecaster.forecast
    obs = mgr.weather_at_place(place)
    weather = obs.weather
    temperature = weather.temperature(unit='celsius')['temp']
    if unit == 'Celsius':
        unit_c = 'celsius'
    else:
        unit_c = 'fahrenheit'

    for weather in forecast:
        day = datetime.utcfromtimestamp(weather.reference_time())
        date1 = day.date()
        if date1 not in dates_2:
            dates_2.append(date1)
            min_t.append(None)
            max_t.append(None)
            days.append(date1)
            temps.append(None)
        temperature = weather.temperature(unit_c)['temp']
        if not temps[-1]:
            temps[-1] = temperature
        if not min_t[-1] or temperature < min_t[-1]:
            min_t[-1] = temperature
        if not max_t[-1] or temperature > max_t[-1]:
            max_t[-1] = temperature
    df = pd.DataFrame(list(zip(days,temps)),
               columns =['days', 'Temperature'])
    obs = mgr.weather_at_place(place)
    weather = obs.weather
    st.title(f"📍 Weather at {place[0].upper() + place[1:]} currently: ")
    if unit_c == 'celsius':
        st.write(f"## 🌡️ Temperature: {temperature} °C")
    else:
        st.write(f"## 🌡️  Temperature: {temperature} F")
    st.write(f"## ☁️ Sky: {weather.detailed_status}")
    st.write(f"## 🌪  Wind Speed: {round(weather.wind(unit='km_hour')['speed'])} km/h")
    st.write(f"### ⛅️Sunrise Time :     {weather.sunrise_time(timeformat='iso')} GMT")
    st.write(f"### ☁️  Sunset Time :      {weather.sunset_time(timeformat='iso')} GMT")

    # Expected Temperature Alerts
    st.title("❄️Expected Temperature Changes/Alerts: ")
    if forecaster.will_have_fog():
        st.write("### ▶️FOG ALERT🌁!!")
    if forecaster.will_have_rain():
        st.write("### ▶️RAIN ALERT☔!!")
    if forecaster.will_have_storm():
        st.write("### ▶️STORM ALERT⛈️!!")
    if forecaster.will_have_snow():
        st.write("### ▶️ SNOW ALERT❄️!!")
    if forecaster.will_have_tornado():
        st.write("### ▶️TORNADO ALERT🌪️!!")
    if forecaster.will_have_hurricane():
        st.write("### ▶️HURRICANE ALERT🌀")
    if forecaster.will_have_clear():
        st.write("### ▶️CLEAR WEATHER PREDICTED🌞!!")
    if forecaster.will_have_clouds():
        st.write("### ▶️CLOUDY SKIES⛅")

    st.write('                ')
    st.write('                ')

# Main function

def weather_detail(place, unit, g_type):
    mgr = owm.weather_manager()
    days = []
    dates_2 = []
    min_t = []
    max_t = []
    temps =[]
    hum=[]
    forecaster = mgr.forecast_at_place(place, '3h')
    forecast = forecaster.forecast
    obs = mgr.weather_at_place(place)
    weather = obs.weather
    temperature = weather.temperature(unit='celsius')['temp']
    if unit == 'Celsius':
        unit_c = 'celsius'
    else:
        unit_c = 'fahrenheit'

    for weather in forecast:
        day = datetime.utcfromtimestamp(weather.reference_time())
        date1 = day.date()
        if date1 not in dates_2:
            dates_2.append(date1)
            min_t.append(None)
            max_t.append(None)
            days.append(date1)
            temps.append(None)
            hum.append(None)
        temperature = weather.temperature(unit_c)['temp']
        humidity = weather.humidity
        if not temps[-1]:
            temps[-1] = temperature
            hum[-1] = humidity
        if not min_t[-1] or temperature < min_t[-1]:
            min_t[-1] = temperature
        if not max_t[-1] or temperature > max_t[-1]:
            max_t[-1] = temperature
    df = pd.DataFrame(list(zip(days,temps,hum)),
               columns =['Days', 'Temperature','Humidity'])
    if g_type == "Display Content":
        display_detail(place,unit)
    elif g_type == "Temperature Forecast":
        plot_temperature(df,min_t,max_t,days)
    elif g_type == "Humidity Forecast":
        plot_rain(df)
   
if b:
    if place != "":
        try:
            weather_detail(place, unit, g_type)

        except NotFoundError:
            st.write("Please enter a Valid city name")



