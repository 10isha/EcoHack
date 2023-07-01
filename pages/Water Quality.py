import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib

st.set_page_config(layout="centered")
st.title("Is the Water Potable?")



st.header("Select your contamination levels and Our model will tell you")
col1, col2 = st.columns(2)
with col1:
   hardness = st.slider("Hardness",50,350)
   solids = st.slider("Solids",320,62000)
   chloramines = st.slider("Chloramines",0,13)
with col2:
   conductivity = st.slider("Conductivity",180,800)
   organic = st.slider("Carbon",0,30)
   turbidity = st.slider("Turbidity",0,7)
b = st.button("SUBMIT")

X = [[hardness,solids,chloramines,conductivity,organic,turbidity]]
# X =[[175.762646	,33155.578218,	7.350233,	432.044783,	11.039070,	3.298875	]]
loaded_model = joblib.load('model_water.sav')
answer=""

if b:
   answer = loaded_model.predict(X)
   if answer[0]== 1 :
      st.success("The Water is Potable!")
   else:
      st.error("The Contamination level is High!")