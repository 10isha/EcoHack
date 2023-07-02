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
import streamlit as st
from gtts import gTTS
from io import BytesIO
sound_file = BytesIO()

# Streamlit Display
st.set_page_config(
    page_title="Weather Forecast",
    page_icon="✅",
    layout="centered",
)
st.title(" 📅 WEATHER FORECASTER 🌥️ ☔ ")

st.header("🌐 Enter the name of City and Select Temperature Unit")
place = st.text_input("NAME OF THE CITY 🌆 ", " ")
unit = st.selectbox(" SELECT TEMPERATURE UNIT 🌡 ", ("Celsius", "Fahrenheit"))
b = st.button("SUBMIT")

# To deceive error of pyplot global warning
st.set_option('deprecation.showPyplotGlobalUse', False)



# Main function

def weather_detail(place, unit):
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
    weather = obs.weather
    st.title(f"📍 Weather at {place[0].upper() + place[1:]} currently: ")
    if unit_c == 'celsius':
        st.write(f"## 🌡️ Temperature: {temperature} °C")
    else:
        st.write(f"## 🌡️  Temperature: {temperature} F")
    st.write(f"## ☁️ Sky: {weather.detailed_status}")
    st.write(f"## 🌪  Wind Speed: {round(weather.wind(unit='km_hour')['speed'])} km/h")
    st.write(f"### ⛅️Sunrise Time : {weather.sunrise_time(timeformat='iso')} GMT")
    st.write(f"### ☁️  Sunset Time : {weather.sunset_time(timeformat='iso')} GMT")
    # Expected Temperature Alerts
    st.title("❄️Expected Temperature Changes/Alerts: ")
    text=""
    if forecaster.will_have_fog():
        text = "FOG ALERT"
        st.write("### ▶️FOG ALERT🌁!!")
    if forecaster.will_have_rain():
        text = "RAIN ALERT"
        st.write("### ▶️RAIN ALERT☔!!")
    if forecaster.will_have_storm():
        text = "STORM ALERT"
        st.write("### ▶️STORM ALERT⛈️!!")
    if forecaster.will_have_snow():
        text = "SNOW ALERT"
        st.write("### ▶️ SNOW ALERT❄️!!")
    if forecaster.will_have_tornado():
        text = "TORNADO ALERT"
        st.write("### ▶️TORNADO ALERT🌪️!!")
    if forecaster.will_have_hurricane():
        text = "HURRICANE ALERT"
        st.write("### ▶️HURRICANE ALERT🌀")
    if forecaster.will_have_clear():
        text = "CLEAR WEATHER PREDICTED"
        st.write("### ▶️CLEAR WEATHER PREDICTED🌞!!")
    if forecaster.will_have_clouds():
        text = "CLOUDY SKIES"
        st.write("### ▶️CLOUDY SKIES⛅")
    tts = gTTS("The temperature at" +place+ "is" +str(temperature)+ "The sky has" + weather.detailed_status + "There is an Alert for" + text , lang='en')
    tts.write_to_fp(sound_file)
    st.audio(sound_file)
    st.write('                ')
    st.write("Temperature Forecast")
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
    st.write('                  ')
    st.write("Humidity Forecast")
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
    st.write('                 ')
    i = 0
    st.write(f"# 📆 Date :  Max - Min  ({unit})")
    for obj in days:
        ta = (obj.strftime("%d/%m"))
        st.write(f'### ➡️ {ta} :\t   ({max_t[i]} - {min_t[i]})')
        i += 1
    

if b:
    if place != "":
        try:
            weather_detail(place, unit)
        except NotFoundError:
            st.write("Please enter a Valid city name")
     


