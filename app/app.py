
# import streamlit as st
# from PIL import Image
# from model import load_model
# from predict import predict
# import pathlib


# # Temporary redirect PosixPath to WindowsPath
# temp = pathlib.PosixPath
# pathlib.PosixPath = pathlib.WindowsPath

# st.title("Pneumonia Detection from Chest X-rays")
# st.write("Upload a chest X-ray image to get a prediction.")

# model = load_model()

# # Restore PosixPath
# pathlib.PosixPath = temp

# uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# if uploaded_file is not None:

#     # Temporary redirect PosixPath to WindowsPath again during prediction
#     pathlib.PosixPath = pathlib.WindowsPath

#     image = Image.open(uploaded_file)
#     st.image(image, caption='Uploaded Image.', use_column_width=True)
#     st.write("")
#     st.write("Classifying...")

#     img_path = f"data/{uploaded_file.name}"
#     image.save(img_path)

#     # Restore PosixPath after prediction
#     pathlib.PosixPath = temp
    
#     label = predict(model, img_path)
#     st.write(f"Prediction: {label}")


import streamlit as st
from PIL import Image
from model import load_model, load_xray_detector
from predict import predict, is_xray
import pathlib

import requests
from io import BytesIO

# Set the page title
st.set_page_config(page_title="CLAARITY PROJECT CXR PNEUMONIA DETECTOR")

# List of image URLs from your GitHub repository
image_urls = [
    "https://github.com/Promisekel/cxr_scans/blob/main/image1.jpg?raw=true",
    "https://github.com/Promisekel/cxr_scans/blob/main/image2.jpg?raw=true",
    # Add more image URLs as needed
]

# Dropdown to select an image
selected_image_url = st.selectbox("Select an image", image_urls)

# Load selected image
if selected_image_url:
    response = requests.get(selected_image_url)
    image = Image.open(BytesIO(response.content))
    st.image(image, caption="Selected Image", use_column_width=True)

    # Load models
    model, xray_detector = load_models()
    
    # Predict pneumonia if it's an X-ray
    st.write("Checking if the image is an X-ray...")
    img_path = f"data/selected_image.jpg"  # Temporary path for prediction
    image.save(img_path)

    if is_xray(xray_detector, img_path):
        st.write("Image is an X-ray. Classifying for pneumonia...")
        label = predict(model, img_path)
        st.write(f"Prediction: {label}")
    else:
        st.write("The selected image is not an X-ray. Please select a chest X-ray image.")

