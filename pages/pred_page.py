import streamlit as st 
from PIL import Image
import numpy as np
import tempfile

from src.prediction.pred import Detector

st.header("Vid")


uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:

    tfile = tempfile.NamedTemporaryFile(delete=False) 
    tfile.write(uploaded_file.read())

    detect = Detector(vid_path=tfile.name, model_path="yolov5/runs/train/yolov5s_results/weights/best.pt")

    detect()



