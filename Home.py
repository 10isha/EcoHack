import streamlit as st
import json
import requests
from streamlit_lottie import st_lottie
st.set_page_config(layout="wide")
st.title(":green[EcoHack]")
st.header("Your neighborhood eco app, making a difference one hack at a time")
st.text("EcoHack is an app that helps you protect the environment.")

st.divider()

col1,col2 = st.columns(2)

with col1:
    st.title("You can:")
    st.subheader(":white_check_mark: Check Air Quality")
    st.subheader(":white_check_mark: Know your :green[Biodiversity]")
    st.subheader(":white_check_mark: Find the Soil Type")
    st.subheader(":white_check_mark: Check if :blue[Water] is Potable")
    st.subheader(":white_check_mark: Track :blue[Water] Quality over the years")
    st.subheader(":white_check_mark: Check Weather Forecast")
   

with col2:
    url = requests.get(
        "https://assets8.lottiefiles.com/packages/lf20_wW88AJkEP5.json")
    url_json = dict()
    if url.status_code == 200:
        url_json = url.json()
    else:
        print("Error in URL")
    st_lottie(url_json,
		# change the direction of our animation
		reverse=True,
		# height and width of animation
		height=400,
		width=400,
		# speed of animation
		speed=1,
		# means the animation will run forever like a gif, and not as a still image
		loop=True,
		# quality of elements used in the animation, other values are "low" and "medium"
		quality='high',
		# THis is just to uniquely identify the animation
		key='Car'
	)

