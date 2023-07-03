import streamlit as st
import matplotlib.pyplot as plt
import torch
from PIL import Image

st.set_page_config(
    page_title="Soil Identification",
    page_icon="✅",
    layout="wide",
)
st.title(":green[Biodiversity] Tracker")
st.header("Know your Biodiversity")
st.text("Upload an Image of the Biodiversity in your area and know their type")
# Loading in yolov5s - you can switch to larger models such as yolov5m or yolov5l, or smaller such as yolov5n

uploaded_file1 = st.file_uploader("Choose an Image", type="jpg")
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')

if uploaded_file1 is not None:
    image1 = Image.open(uploaded_file1)
    results = model(image1)
    fig, ax = plt.subplots(figsize=(16, 12))
    ax.imshow(results.render()[0])
    st.pyplot(fig)
