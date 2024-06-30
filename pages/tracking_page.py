import streamlit as st 
from PIL import Image
import numpy as np

def load_image(img):
    im = Image.open(img)
    image = np.array(im)
    return image

st.title("This is the page used to track the Models Preformance")

# /content/yolov5/runs/train/yolov5s_results/results.png

st.image('yolov5/runs/train/yolov5s_results/results.png', caption='Model Preformance')
