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
from PIL import Image
from io import BytesIO
from model import load_model, load_xray_detector
from predict import predict, is_xray
import requests
import pathlib

!pip install requests

# Set the page title
st.set_page_config(page_title="CLAARITY PROJECT CXR PNEUMONIA DETECTOR")

# Temporary redirect PosixPath to WindowsPath
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

@st.cache(allow_output_mutation=True)
def load_models():
    model = load_model()
    xray_detector = load_xray_detector()
    return model, xray_detector

st.title("CLAARITY PROJECT CXR PNEUMONIA DETECTOR")
st.write("Enter the Google Drive URL of the chest X-ray to predict pneumonia outcome.")

# Load models
model, xray_detector = load_models()

# Input for Google Drive URL
google_drive_url = st.text_input("Enter Google Drive image URL:")

# Extract image ID and generate a direct download link
def fetch_image_from_drive(google_drive_url):
    file_id = google_drive_url.split("/d/")[1].split("/")[0]
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(download_url)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        return image
    else:
        st.write("Failed to fetch the image. Please check the URL.")
        return None

# Predict and display results
if google_drive_url:
    image = fetch_image_from_drive(google_drive_url)
    if image:
        st.image(image, caption='Fetched Image.', use_column_width=True)
        st.write("Checking if the image is an X-ray...")

        # Save temporarily for prediction
        img_path = "data/fetched_image.png"
        image.save(img_path)

        if is_xray(xray_detector, img_path):
            st.write("Image is an X-ray. Classifying for pneumonia...")
            label = predict(model, img_path)
            st.write(f"Prediction: {label}")
        else:
            st.write("Uploaded image is not an X-ray. Please upload a chest X-ray image.")

# Restore PosixPath after prediction
pathlib.PosixPath = temp
