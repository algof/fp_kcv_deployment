from PIL import Image
from io import BytesIO
from ultralytics import YOLO
import numpy as np
import streamlit as st

model = YOLO("model.pt")

st.title("Superhero Predictions")
st.write("Upload an image and look what happen!!")

uploaded_file = st.file_uploader("📂 Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
	image = Image.open(uploaded_file)
	image_array = np.array(image)
	
	st.image(image, caption="🖼 Uploaded Image", use_column_width=True)
	
	# Melakukan prediksi
	results = model(image_array, verbose=False)
	pred = results[0]

	st.write("🏆 Top Predictions:")
	st.write(f"{pred.names[pred.probs.top1]}")