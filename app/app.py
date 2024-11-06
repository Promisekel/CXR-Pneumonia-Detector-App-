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

# Set the page title
st.set_page_config(page_title="CLAARITY PROJECT CXR PNEUMONIA DETECTOR")

# GitHub image URLs (ensure URLs end with ?raw=true)
image_urls = [
    "https://github.com/Promisekel/cxr_scans/blob/main/image1.jpg?raw=true",
    "https://github.com/Promisekel/cxr_scans/blob/main/image2.jpg?raw=true",
    # Add all 10 image URLs here
]

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

    # Ensure the directory exists
    img_dir = pathlib.Path("data")
    img_dir.mkdir(parents=True, exist_ok=True)  # Create 'data' directory if it doesn't exist

    # Ensure the file has an extension (e.g., .jpg)
    img_path = img_dir / f"{image_name}"
    if not img_path.suffix:
        img_path = img_path.with_suffix(".jpg")  # Default to .jpg if no extension exists

    # Save the image temporarily
    try:
        image.save(img_path)
    except ValueError as e:
        st.error(f"Error saving the image: {e}")
        return

    # Perform X-ray check and prediction
    if is_xray(xray_detector, img_path):
        st.write("Image confirmed as X-ray. Classifying for pneumonia, please wait...")
        label = predict(model, img_path)
        st.write(f"Prediction: {label}")
    else:
        st.write("Selected image is not a chest X-ray. Please upload a valid chest X-ray image.")

# Display selected image
if selected_image_url:
    try:
        response = requests.get(selected_image_url)
        response.raise_for_status()  # Check if request was successful
        image = Image.open(BytesIO(response.content))
        predict_and_display_results(image, selected_image_url.split("/")[-1])
    except UnidentifiedImageError:
        st.error("Error: The selected URL did not return a valid image. Please check the URL.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching the image: {e}")
