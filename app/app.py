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
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO
import pathlib
import streamlit as st
from PIL import Image
from model import load_model
from predict import predict
# import pathlib

import streamlit as st
from PIL import Image, UnidentifiedImageError
from model import load_model, load_xray_detector
from predict import predict, is_xray
import requests
from io import BytesIO

# Load models with caching
@st.cache(allow_output_mutation=True)
def load_models():
    model = load_model()
    xray_detector = load_xray_detector()
    return model, xray_detector

# Function to download and verify image from Google Drive
def download_image_from_drive(url):
    try:
        # Extract the file ID from the Google Drive URL
        file_id = url.split('/')[-2]
        download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        
        # Send a GET request to download the image
        response = requests.get(download_url)
        response.raise_for_status()  # Check for HTTP errors

        # Verify if response content is an image
        try:
            image = Image.open(BytesIO(response.content))
            return image
        except UnidentifiedImageError:
            st.error("The file downloaded is not recognized as an image. Ensure the URL is correct and public.")
            return None
    except Exception as e:
        st.error(f"An error occurred while downloading the image: {e}")
        return None

# Streamlit app setup
st.set_page_config(page_title="CLAARITY PROJECT CXR PNEUMONIA DETECTOR")
st.title("CLAARITY PROJECT CXR PNEUMONIA DETECTOR")
st.write("Paste a Google Drive image URL or upload a chest X-ray to predict pneumonia outcome.")

# Load models
model, xray_detector = load_models()

# Google Drive URL input
drive_url = st.text_input("Paste Google Drive image URL here:")

if drive_url:
    image = download_image_from_drive(drive_url)
    if image:
        st.image(image, caption='Downloaded Image', use_column_width=True)
        st.write("Checking if the image is an X-ray...")
        
        # Temporarily save image and predict
        img_path = "temp_image.jpg"
        image.save(img_path)

        if is_xray(xray_detector, img_path):
            st.write("Image is an X-ray. Classifying for pneumonia...")
            label = predict(model, img_path)
            st.write(f"Prediction: {label}")
        else:
            st.write("Uploaded image is not an X-ray. Please upload a chest X-ray image.")
else:
    st.write("Provide a Google Drive URL or upload an image to proceed.")
