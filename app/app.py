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
from PIL import Image
import requests
from io import BytesIO
from model import load_model, load_xray_detector
from predict import predict, is_xray

# Set the page title
st.set_page_config(page_title="CLAARITY PROJECT CXR PNEUMONIA DETECTOR")

# GitHub image URLs
image_urls = [
    "https://github.com/Promisekel/cxr_scans/blob/main/4-normal-healthy-chest-x-ray-photostock-israel-canvas-print.jpg?raw=true",
    "https://github.com/Promisekel/cxr_scans/blob/main/WhatsApp%20Image%202024-09-24%20at%2010.37.48_b40dff0a.jpg?raw=true",
    # Add all 10 image URLs here
]

# Temporary redirect PosixPath to WindowsPath
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

# Function to load models
@st.cache(allow_output_mutation=True)
def load_models():
    model = load_model()
    xray_detector = load_xray_detector()
    return model, xray_detector

# Set up the app interface
st.title("CLAARITY PROJECT CXR PNEUMONIA DETECTOR")
st.write("Select a chest X-ray image to predict the likelihood of pneumonia.")

# Load models
model, xray_detector = load_models()

# Dropdown to select an image
selected_image_url = st.selectbox("Select an image from GitHub:", image_urls)

# Function to predict and display results
def predict_and_display_results(image, image_name):
    st.image(image, caption=image_name, use_column_width=True)
    st.write("Analyzing the image to confirm it’s an X-ray...")

    # Save the image temporarily
    img_path = f"data/{image_name}"
    image.save(img_path)

    # Perform X-ray check and prediction
    if is_xray(xray_detector, img_path):
        st.write("Image confirmed as X-ray. Classifying for pneumonia...")
        label = predict(model, img_path)
        st.write(f"Prediction: {label}")
    else:
        st.write("Selected image is not a chest X-ray. Please upload a valid chest X-ray image.")

# Display selected image
if selected_image_url:
    response = requests.get(selected_image_url)
    image = Image.open(BytesIO(response.content))
    predict_and_display_results(image, selected_image_url.split("/")[-1])

# Restore PosixPath
pathlib.PosixPath = temp

